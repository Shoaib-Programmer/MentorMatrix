import os
import json
from flask import Blueprint, request, jsonify, flash, redirect, url_for, render_template, current_app, Response
from werkzeug.utils import secure_filename
from models import db
from notes import transcribe_audio, convert_pdf_to_text, get_video_id_from_url, get_transcript_from_youtube
import logging
from icecream import ic
from pytube import YouTube

logging.basicConfig(level=logging.DEBUG)

transcribe_blueprint = Blueprint('transcribe', __name__)


def save_file(file, folder):
    """
    Saves the uploaded file to the specified folder and returns its full path.
    """
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file.save(file_path)
    return file_path, filename


@transcribe_blueprint.route('/upload_audio', methods=['POST'])
def upload_audio():

    logging.debug("Upload_audio route called.")

    if 'audio' not in request.files:
        logging.error("No audio file in request.")
        return jsonify({"error": "No audio file uploaded."}), 400

    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded."}), 400

    audio_file = request.files['audio']
    try:
        # Save the file
        file_path, filename = save_file(audio_file, 'audio')

        # Transcribe the audio
        transcript = transcribe_audio(file_path)

        # Get or derive the title
        title = request.form.get('title', filename)

        # Save the transcript and file metadata in the database
        db.execute('INSERT INTO transcripts (title, content) VALUES (?, ?)', title, transcript)
        transcript_id = db.execute(
            'SELECT id FROM transcripts WHERE content = ?', transcript)[0]['id']
        db.execute('''
            INSERT INTO files (transcript_id, file_type, name, uploaded_at)
            VALUES (?, 'audio', ?, CURRENT_TIMESTAMP)
        ''', transcript_id, filename)

        return redirect(url_for('notes.generate_notes', transcript_id=transcript_id))
    except Exception as e:
        return jsonify({"error": f"Error processing audio file: {e}"}), 500


@transcribe_blueprint.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        flash("No PDF file uploaded.", "error")
        return redirect(url_for('dashboard.dashboard'))

    pdf_file = request.files['pdf']
    try:
        # Save the file
        file_path, filename = save_file(pdf_file, 'pdfs')

        # Extract text from the PDF
        extracted_text = convert_pdf_to_text(file_path)
        if not extracted_text.strip():
            flash("Failed to extract text from the PDF.")
            return redirect(url_for('dashboard.dashboard'))

        # Get or derive the title
        title = request.form.get('title', filename)

        # Save the transcript and file metadata in the database
        db.execute('INSERT INTO transcripts (title, content) VALUES (?, ?)', title, extracted_text)
        transcript_id = db.execute(
            'SELECT id FROM transcripts WHERE content = ?', extracted_text)[0]['id']
        db.execute('''
            INSERT INTO files (transcript_id, file_type, name, uploaded_at)
            VALUES (?, 'pdf', ?, CURRENT_TIMESTAMP)
        ''', transcript_id, filename)

        flash("PDF uploaded and processed successfully.", "success")
    except Exception as e:
        flash(f"Error processing PDF file: {e}", "error")

    return redirect(url_for('notes.generate_notes', transcript_id=transcript_id))


@transcribe_blueprint.route('/upload_youtube', methods=['POST'])
def upload_youtube():
    youtube_url = request.form.get('youtube_url')
    if not youtube_url:
        flash("Missing YouTube URL.", "error")
        return redirect(url_for('dashboard.dashboard'))

    try:
        # Fetch video title using pytube
        yt = YouTube(youtube_url)
        title = yt.title

        def generate_transcription():
            try:
                for partial_transcript, progress in get_transcript_from_youtube(youtube_url):
                    yield f"data: {json.dumps({'progress': progress, 'transcript': partial_transcript})}\n\n"
                
                # Save transcript to the database after processing
                final_transcript = partial_transcript
                db.execute('INSERT INTO transcripts (title, content) VALUES (?, ?)', title, final_transcript)
                transcript_id = db.execute(
                    'SELECT id FROM transcripts WHERE content = ?', final_transcript
                )[0]['id']
                db.execute(
                    '''
                    INSERT INTO files (transcript_id, file_type, name, metadata, uploaded_at)
                    VALUES (?, 'youtube', ?, ?, CURRENT_TIMESTAMP)
                    ''',
                    transcript_id, title, f'{{"url": "{youtube_url}", "video_id": "{yt.video_id}"}}'
                )

            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return Response(generate_transcription(), mimetype='text/event-stream')

    except Exception as e:
        flash(f"Error processing YouTube URL: {e}", "error")
        return redirect(url_for('notes.generate_notes'))


@transcribe_blueprint.route('/transcript')
def transcript():
    # Query and group files by type
    files = db.execute('''
        SELECT id, file_type, name, metadata, uploaded_at
        FROM files
    ''')
    grouped_files = {
        "audio": [f for f in files if f['file_type'] == 'audio'],
        "youtube": [f for f in files if f['file_type'] == 'youtube'],
        "pdf": [f for f in files if f['file_type'] == 'pdf']
    }

    ic(grouped_files)

    return render_template(
        'transcript.html',
        grouped_files=grouped_files,
        current_route='transcript'
    )

@transcribe_blueprint.route('/view_transcript/<int:file_id>')
def view_transcript(file_id):
    # Fetch the transcript based on the file_id from the database
    transcript = db.execute('SELECT title, content FROM transcripts WHERE id = ?', file_id)

    if not transcript:
        return jsonify({"error": "Transcript not found."}), 404

    # Extract title and content from the fetched transcript
    transcript_name = transcript[0]['title']
    content = transcript[0]['content']

    # Render the view_transcript.html template with the fetched transcript name and content
    return render_template('view_transcript.html', transcript_name=transcript_name, content=content)
