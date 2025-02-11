import os
from flask import (  # type: ignore
    Blueprint,
    request,
    jsonify,
    flash,
    redirect,
    url_for,
    render_template,
    current_app,
)
from werkzeug.utils import secure_filename  # type: ignore
from app.models import db
from app.notes import (
    transcribe_audio,
    convert_pdf_to_text,
    get_video_id_from_url,
    get_transcript_from_youtube,
)
import logging
from typing import Optional
from dotenv import load_dotenv  # type: ignore
from icecream import ic  # type: ignore

from googleapiclient.discovery import (  # type: ignore
    build,
)  # Import YouTube Data API client

import googleapiclient.discovery_cache  # type: ignore

googleapiclient.discovery_cache.DISABLE_CACHE = True

load_dotenv()

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')


logging.basicConfig(level=logging.DEBUG)

transcribe_blueprint = Blueprint("transcribe", __name__)


def save_file(file, folder):
    """
    Saves the uploaded file to the specified folder and returns its full path.
    """
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], folder, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file.save(file_path)
    return file_path, filename


@transcribe_blueprint.route("/upload_audio", methods=["POST"])
def upload_audio():
    logging.debug("Upload_audio route called.")

    if "audio" not in request.files:
        logging.error("No audio file in request.")
        return jsonify({"error": "No audio file uploaded."}), 400

    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded."}), 400

    audio_file = request.files["audio"]
    try:
        # Save the file
        file_path, filename = save_file(audio_file, "audio")

        # Transcribe the audio
        transcript = transcribe_audio(file_path)

        # Get or derive the title
        title = request.form.get("title", filename)

        # Save the transcript and file metadata in the database
        db.execute(
            "INSERT INTO transcripts (title, content) VALUES (?, ?)", title, transcript
        )
        transcript_id = db.execute(
            "SELECT id FROM transcripts WHERE content = ?", transcript
        )[0]["id"]
        db.execute(
            """
            INSERT INTO files (transcript_id, file_type, name, uploaded_at)
            VALUES (?, 'audio', ?, CURRENT_TIMESTAMP)
        """,
            transcript_id,
            filename,
        )

        return redirect(url_for("notes.generate_notes", transcript_id=transcript_id))
    except Exception as e:
        return jsonify({"error": f"Error processing audio file: {e}"}), 500


@transcribe_blueprint.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    if "pdf" not in request.files:
        flash("No PDF file uploaded.", "error")
        return redirect(url_for("dashboard.dashboard"))

    pdf_file = request.files["pdf"]
    try:
        # Save the file
        file_path, filename = save_file(pdf_file, "pdfs")

        # Extract text from the PDF
        extracted_text = convert_pdf_to_text(file_path)
        if not extracted_text.strip():
            flash("Failed to extract text from the PDF.")
            return redirect(url_for("dashboard.dashboard"))

        # Get or derive the title
        title = request.form.get("title", filename)

        # Save the transcript and file metadata in the database
        db.execute(
            "INSERT INTO transcripts (title, content) VALUES (?, ?)",
            title,
            extracted_text,
        )
        transcript_id = db.execute(
            "SELECT id FROM transcripts WHERE content = ?", extracted_text
        )[0]["id"]
        db.execute(
            """
            INSERT INTO files (transcript_id, file_type, name, uploaded_at)
            VALUES (?, 'pdf', ?, CURRENT_TIMESTAMP)
        """,
            transcript_id,
            filename,
        )

        flash("PDF uploaded and processed successfully.", "success")
    except Exception as e:
        flash(f"Error processing PDF file: {e}", "error")

    return redirect(url_for("notes.generate_notes", transcript_id=transcript_id))


# Helper function to fetch the video title
def fetch_youtube_video_title(video_id: str) -> Optional[str]:
    """
    Fetches the title of a YouTube video using the YouTube Data API.
    :param video_id: YouTube video ID.
    :return: Video title, or None if an error occurs.
    """
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY, cache_discovery=False)
        response = youtube.videos().list(part="snippet", id=video_id).execute()
        if "items" in response and len(response["items"]) > 0:
            return response["items"][0]["snippet"]["title"]
        return None
    except Exception as e:
        logging.error(f"Failed to fetch video title: {e}")
        return None


@transcribe_blueprint.route("/upload_youtube", methods=["POST"])
def upload_youtube():
    logging.debug("Upload_youtube route called.")

    youtube_url = request.json.get(
        "youtube_url"
    )  # Expecting JSON body with `youtube_url`
    if not youtube_url:
        flash("No YouTube URL provided.", "error")
        return redirect(url_for("notes.notes"))

    try:
        # Step 1: Extract video ID from URL
        video_id = get_video_id_from_url(youtube_url)
        if not video_id:
            flash("Invalid YouTube URL.", "error")
            return redirect(url_for("notes.notes"))

        # Step 2: Fetch the video title
        title = fetch_youtube_video_title(video_id)
        if not title:
            flash("Could not fetch video title.", "error")
            return redirect(url_for("notes.notes"))

        # Step 3: Get the transcript
        transcript = get_transcript_from_youtube(youtube_url)
        ic(transcript)
        if not transcript.strip():
            flash(
                "Failed to generate transcript from the provided YouTube URL.", "error"
            )
            return redirect(url_for("notes.notes"))

        # Step 4: Save the transcript and file metadata to the database
        db.execute(
            "INSERT INTO transcripts (title, content) VALUES (?, ?)", title, transcript
        )
        transcript_id = db.execute(
            "SELECT id FROM transcripts WHERE content = ?", transcript
        )[0]["id"]
        db.execute(
            """
            INSERT INTO files (transcript_id, file_type, name, uploaded_at)
            VALUES (?, 'youtube', ?, CURRENT_TIMESTAMP)
            """,
            transcript_id,
            youtube_url,
        )

        # Redirect to notes.generate_notes with the transcript_id
        return redirect(url_for("notes.generate_notes", transcript_id=transcript_id))
    except Exception as e:
        logging.error(f"Error processing YouTube URL: {e}")
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for("notes.notes"))


@transcribe_blueprint.route("/transcript")
def transcript():
    # Query and group files by type
    files = db.execute("""
        SELECT id, file_type, name, metadata, uploaded_at
        FROM files
    """)
    grouped_files = {
        "audio": [f for f in files if f["file_type"] == "audio"],
        "youtube": [f for f in files if f["file_type"] == "youtube"],
        "pdf": [f for f in files if f["file_type"] == "pdf"],
    }

    ic(grouped_files)

    return render_template(
        "transcript.html", grouped_files=grouped_files, current_route="transcript"
    )


@transcribe_blueprint.route("/view_transcript/<int:file_id>")
def view_transcript(file_id):
    # Fetch the transcript based on the file_id from the database
    transcript = db.execute(
        "SELECT title, content FROM transcripts WHERE id = ?", file_id
    )

    if not transcript:
        return jsonify({"error": "Transcript not found."}), 404

    # Extract title and content from the fetched transcript
    transcript_name = transcript[0]["title"]
    content = transcript[0]["content"]

    # Render the view_transcript.html template with the fetched transcript name and content
    return render_template(
        "view_transcript.html",
        transcript_name=transcript_name,
        content=content,
        current_route="transcript",
    )
