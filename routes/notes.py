from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from datetime import datetime
from notes import summarize_text

notes_blueprint = Blueprint('notes', __name__)


@notes_blueprint.route('/notes')
def notes():
    # Fetch notes along with associated files and transcript titles

    notes_data = db.execute('''
        SELECT
            notes.id,
            notes.title AS note_title,
            notes.content AS note_content,
            notes.created_at,
            files.name AS file_name,
            files.file_type,
            files.metadata,
            transcripts.title AS transcript_title
        FROM notes
        LEFT JOIN files ON notes.transcript_id = files.transcript_id
        LEFT JOIN transcripts ON notes.transcript_id = transcripts.id
    ''')
    return render_template('notes.html', notes=notes_data, current_route='notes')


@notes_blueprint.route('/generate_notes/<int:transcript_id>', methods=['GET', 'POST'])
def generate_notes(transcript_id):
    # Fetch relevant file details and transcript content
    transcript_data = db.execute('''
        SELECT
            transcripts.title AS transcript_title,
            transcripts.content AS transcript_content,
            files.file_type,
            files.metadata
        FROM transcripts
        LEFT JOIN files ON transcripts.id = files.transcript_id
        WHERE transcripts.id = ? AND files.file_type IN ('audio', 'youtube', 'pdf')
    ''', transcript_id)

    if not transcript_data:
        flash("No associated files or transcript found for this ID.", "error")
        return redirect(url_for('notes.notes'))

    # Extract data from query result
    transcript_title = transcript_data[0]['transcript_title']
    transcript_content = transcript_data[0]['transcript_content']

    # For later
    file_type = transcript_data[0]['file_type']
    metadata = transcript_data[0].get('metadata', '')

    if not transcript_content:
        flash("Transcript content is empty.", "error")
        return redirect(url_for('notes.notes'))

    # Summarize the transcript content
    try:
        note_content = summarize_text(transcript_content)
    except Exception as e:
        flash(f"Error summarizing the transcript: {e}", "error")
        return redirect(url_for('notes.notes'))

    # Save the summarized note in the database
    try:
        db.execute('''
            INSERT INTO notes (transcript_id, title, content, created_at, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ''', transcript_id, transcript_title, note_content)
        flash("Notes generated successfully.", "success")
    except Exception as e:
        flash(f"Error saving the note: {e}", "error")

    return redirect(url_for('notes.notes'))


@notes_blueprint.route('/add_note', methods=['POST'])
def add_note():
    # Get form data
    title = request.form.get('title')
    content = request.form.get('content')
    transcript_id = request.form.get('transcript_id')  # Can be None

    if not title or not content:
        flash("Both title and content are required.", "error")
        return redirect(url_for('notes.notes'))

    # Save note in the database with the associated transcript_id (optional)
    try:
        db.execute('''
            INSERT INTO notes (transcript_id, title, content, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', transcript_id, title, content)
        flash("Note added successfully.", "success")
    except Exception as e:
        flash(f"Error saving the note: {e}", "error")

    return redirect(url_for('notes.notes'))

@notes_blueprint.route('/notes/<int:note_id>')
def view_note(note_id):
    # Fetch the note details by ID
    result = db.execute('''
        SELECT
            notes.title AS note_title,
            notes.content AS note_content,
            notes.created_at,
            files.name AS file_name,
            files.file_type,
            files.metadata,
            transcripts.title AS transcript_title
        FROM notes
        LEFT JOIN files ON notes.transcript_id = files.transcript_id
        LEFT JOIN transcripts ON notes.transcript_id = transcripts.id
        WHERE notes.id = ?
    ''', note_id)

    # Extract the first row if the result is not empty
    note = result[0] if result else None

    if not note:
        flash("Note not found.", "error")
        return redirect(url_for('notes.notes'))

    # Render the note details page
    return render_template('view_note.html', note=note)
