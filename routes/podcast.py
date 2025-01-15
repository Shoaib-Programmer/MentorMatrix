from flask import (  # type: ignore
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
)
from notes.AI import generate_podcast, text_to_podcast
from models import db
from pathlib import Path

podcast_blueprint = Blueprint("podcast", __name__)


@podcast_blueprint.route("/podcast")
def podcast():
    """List all podcasts."""
    podcasts = db.execute("SELECT * FROM podcasts ORDER BY created_at DESC")
    return render_template("podcast.html", current_route="podcast", podcasts=podcasts)


@podcast_blueprint.route("/podcast/<int:podcast_id>")
def podcast_detail(podcast_id):
    """View details of a specific podcast."""
    podcast = db.execute("SELECT * FROM podcasts WHERE id = ?", podcast_id)
    if not podcast:
        flash("Podcast not found!", "error")
        return redirect(url_for("podcast.podcast"))
    return render_template("podcast_detail.html", podcast=podcast[0])


@podcast_blueprint.route("/podcast/generate", methods=["GET", "POST"])
def generate_podcast_route():
    """Generate a new podcast."""
    if request.method == "GET":
        # Render the podcast generation form
        return render_template("generate_podcast.html")

    if request.method == "POST":
        try:
            text = request.form.get("text")
            speaker1 = request.form.get("speaker1", "Adam")
            speaker2 = request.form.get("speaker2", "Bella")

            if not text:
                flash("Text is required to generate a podcast.", "error")
                return redirect(url_for("podcast.generate_podcast_route"))

            # Generate podcast content
            podcast_content = generate_podcast(text, speaker1, speaker2)
            if not podcast_content:
                flash("Failed to generate podcast content.", "error")
                return redirect(url_for("podcast.generate_podcast_route"))

            # Save podcast audio
            save_path = Path("static/podcasts")
            save_path.mkdir(parents=True, exist_ok=True)
            audio_file = (
                save_path
                / f"podcast_{len(db.execute('SELECT * FROM podcasts')) + 1}.mp3"
            )
            text_to_podcast(podcast_content, audio_file, speaker1, speaker2)

            # Save podcast metadata in database
            db.execute(
                "INSERT INTO podcasts (content, path) VALUES (?, ?)",
                podcast_content,
                str(audio_file),
            )

            flash("Podcast generated successfully!", "success")
            return redirect(url_for("podcast.podcast"))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("podcast.generate_podcast_route"))
