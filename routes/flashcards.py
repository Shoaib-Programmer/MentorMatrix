from flask import Blueprint, render_template, request, redirect, url_for, flash
from notes import generate_flashcards
from datetime import datetime
from models import db

flashcards_blueprint = Blueprint('flashcards', __name__)

@flashcards_blueprint.route('/flashcards')
def flashcards():
    """
    Display the list of flashcards from the database, ordered by creation date.
    """
    flashcards = db.execute("SELECT * FROM flashcards ORDER BY created_at DESC")
    return render_template('flashcards.html', flashcards=flashcards)

@flashcards_blueprint.route('/add_flashcard', methods=['POST'])
def add_flashcard():
    """
    Add a new flashcard manually.
    """
    question = request.form.get('question')
    answer = request.form.get('answer')
    
    if not question or not answer:
        flash("Both question and answer fields are required!", "error")
        return redirect(url_for('flashcards.flashcards'))
    
    try:
        db.execute(
            """
            INSERT INTO flashcards (note_id, question, answer, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            None,  # Replace `None` with a valid `transcript_id` if needed
            question,
            answer,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        flash("Flashcard added successfully!", "success")
    except Exception as e:
        flash(f"Error adding flashcard: {e}", "error")
    return redirect(url_for('flashcards.flashcards'))

@flashcards_blueprint.route('/generate_flashcards', methods=['POST'])
def generate_flashcards_route():
    """
    Generate flashcards using the provided text input and number of clusters.
    """
    input_text = request.form.get('input_text')
    num_clusters = request.form.get('num_clusters', type=int, default=5)
    
    if not input_text:
        flash("Please provide text input to generate flashcards.", "error")
        return redirect(url_for('flashcards.flashcards'))
    
    try:
        # Assume `generate_flashcards` takes a list of sentences
        sentences = input_text.split(".")
        generated_flashcards = generate_flashcards(sentences, num_clusters)
        
        # Add generated flashcards to the database
        for cluster in generated_flashcards:
            question = f"Cluster summary: {cluster[0]}"  # Simplify this as needed
            answer = " ".join(cluster)
            db.execute(
                """
                INSERT INTO flashcards (transcript_id, question, answer, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                None,  # Replace `None` with a valid `transcript_id` if applicable
                question,
                answer,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        flash(f"{len(generated_flashcards)} flashcards generated successfully!", "success")
    except Exception as e:
        flash(f"Error generating flashcards: {e}", "error")
    
    return redirect(url_for('flashcards.flashcards'))

@flashcards_blueprint.route('/delete_flashcard/<int:flashcard_id>', methods=['POST'])
def delete_flashcard(flashcard_id):
    """
    Delete a flashcard by its ID.
    """
    try:
        db.execute("DELETE FROM flashcards WHERE id = ?", flashcard_id)
        flash("Flashcard deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting flashcard: {e}", "error")
    return redirect(url_for('flashcards.flashcards'))

@flashcards_blueprint.route('/edit_flashcard/<int:flashcard_id>', methods=['GET', 'POST'])
def edit_flashcard(flashcard_id):
    """
    Edit an existing flashcard.
    """
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        
        if not question or not answer:
            flash("Both question and answer fields are required!", "error")
            return redirect(url_for('flashcards.flashcards'))
        
        try:
            db.execute(
                """
                UPDATE flashcards 
                SET question = ?, answer = ?, updated_at = ?
                WHERE id = ?
                """,
                question,
                answer,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                flashcard_id
            )
            flash("Flashcard updated successfully!", "success")
        except Exception as e:
            flash(f"Error updating flashcard: {e}", "error")
        return redirect(url_for('flashcards.flashcards'))
    
    # For GET requests, fetch the flashcard for editing
    flashcard = db.execute("SELECT * FROM flashcards WHERE id = ?", flashcard_id)
    if not flashcard:
        flash("Flashcard not found.", "error")
        return redirect(url_for('flashcards.flashcards'))
    
    return render_template('edit_flashcard.html', flashcard=flashcard[0])

@flashcards_blueprint.route('/search_flashcards')
def search_flashcards():
    """
    Search flashcards by a query string.
    """
    query = request.args.get('query', '').strip()
    
    if not query:
        flash("Search query cannot be empty.", "error")
        return redirect(url_for('flashcards.flashcards'))
    
    try:
        # Search for flashcards where the question or answer matches the query
        flashcards = db.execute(
            """
            SELECT * FROM flashcards 
            WHERE question LIKE ? OR answer LIKE ?
            ORDER BY created_at DESC
            """,
            f"%{query}%", f"%{query}%"
        )
        return render_template('flashcards.html', flashcards=flashcards, search_query=query)
    except Exception as e:
        flash(f"Error during search: {e}", "error")
        return redirect(url_for('flashcards.flashcards'))
