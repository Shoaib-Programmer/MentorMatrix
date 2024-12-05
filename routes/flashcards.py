from flask import Blueprint, render_template, request, redirect, url_for, flash
from notes import generate_flashcards
from datetime import datetime

flashcards_blueprint = Blueprint('flashcards', __name__)

# In-memory storage for flashcards (replace with a database in production)
flashcards_storage = []

@flashcards_blueprint.route('/flashcards')
def flashcards():
    """
    Display the list of flashcards.
    """
    return render_template('flashcards.html', flashcards=flashcards_storage)

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
    
    flashcard = {
        "question": question,
        "answer": answer,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    flashcards_storage.append(flashcard)
    flash("Flashcard added successfully!", "success")
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
        
        # Add generated flashcards to the storage
        for cluster in generated_flashcards:
            question = f"Cluster summary: {cluster[0]}"  # Simplify this as needed
            answer = " ".join(cluster)
            flashcard = {
                "question": question,
                "answer": answer,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            flashcards_storage.append(flashcard)
        
        flash(f"{len(generated_flashcards)} flashcards generated successfully!", "success")
    except Exception as e:
        flash(f"Error generating flashcards: {e}", "error")
    
    return redirect(url_for('flashcards.flashcards'))
