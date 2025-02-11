from flask import Blueprint, render_template, request, redirect, url_for, flash  # type: ignore
from app.notes import generate_flashcards, get_title, generate_description
from datetime import datetime
from app.models import db
from icecream import ic  # type: ignore

flashcards_blueprint = Blueprint("flashcards", __name__)


@flashcards_blueprint.route("/flashcards")
def flashcards():
    """
    Display the list of flashcards from the database, ordered by creation date.
    Optionally filter by deck.
    """
    deck_id = request.args.get("deck_id")

    if deck_id:
        flashcards = db.execute(
            "SELECT * FROM flashcards WHERE deck_id = ? ORDER BY created_at DESC",
            deck_id,
        )
    else:
        flashcards = db.execute("SELECT * FROM flashcards ORDER BY created_at DESC")

    decks = db.execute(
        "SELECT * FROM decks ORDER BY created_at DESC"
    )  # Get available decks

    return render_template(
        "flashcards.html",
        current_route="flashcards",
        flashcards=flashcards,
        decks=decks,
        selected_deck_id=deck_id,
    )


@flashcards_blueprint.route("/add_flashcard", methods=["POST"])
def add_flashcard():
    """
    Add a new flashcard manually, with an option to choose a deck.
    """
    question = request.form.get("question")
    answer = request.form.get("answer")
    deck_id = request.form.get("deck_id")  # Deck ID to associate the flashcard with

    if not question or not answer or not deck_id:
        flash("Question, answer, note ID, and deck ID are required!", "error")
        return redirect(url_for("flashcards.flashcards"))

    try:
        db.execute(
            """
            INSERT INTO flashcards (deck_id, question, answer, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            deck_id,
            question,
            answer,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        flash("Flashcard added successfully!", "success")
    except Exception as e:
        ic(f"Error adding flashcard: {e}", "error")
        flash(f"Error adding flashcard: {e}", "error")
    return redirect(url_for("flashcards.flashcards"))


@flashcards_blueprint.route("/delete_flashcard/<int:flashcard_id>", methods=["POST"])
def delete_flashcard(flashcard_id):
    """
    Delete a flashcard by its ID.
    """
    try:
        db.execute("DELETE FROM flashcards WHERE id = ?", flashcard_id)
        flash("Flashcard deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting flashcard: {e}", "error")
    return redirect(url_for("flashcards.flashcards"))


@flashcards_blueprint.route(
    "/edit_flashcard/<int:flashcard_id>", methods=["GET", "POST"]
)
def edit_flashcard(flashcard_id):
    """
    Edit an existing flashcard.
    """
    if request.method == "POST":
        question = request.form.get("question")
        answer = request.form.get("answer")
        deck_id = request.form.get("deck_id")  # Deck ID to update with

        if not question or not answer or not deck_id:
            flash(
                "Both question and answer fields, and a deck ID are required!", "error"
            )
            return redirect(url_for("flashcards.flashcards"))

        try:
            db.execute(
                """
                UPDATE flashcards 
                SET question = ?, answer = ?, deck_id = ?, updated_at = ?
                WHERE id = ?
                """,
                question,
                answer,
                deck_id,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                flashcard_id,
            )
            flash("Flashcard updated successfully!", "success")
        except Exception as e:
            flash(f"Error updating flashcard: {e}", "error")
        return redirect(url_for("flashcards.flashcards"))

    # For GET requests, fetch the flashcard for editing
    flashcard = db.execute("SELECT * FROM flashcards WHERE id = ?", flashcard_id)
    if not flashcard:
        flash("Flashcard not found.", "error")
        return redirect(url_for("flashcards.flashcards"))

    decks = db.execute(
        "SELECT * FROM decks ORDER BY created_at DESC"
    )  # Get available decks for selection
    return render_template("edit_flashcard.html", flashcard=flashcard[0], decks=decks)


@flashcards_blueprint.route("/search_flashcards")
def search_flashcards():
    """
    Search flashcards by a query string.
    """
    query = request.args.get("query", "").strip()

    if not query:
        flash("Search query cannot be empty.", "error")
        return redirect(url_for("flashcards.flashcards"))

    try:
        # Search for flashcards where the question or answer matches the query
        flashcards = db.execute(
            """
            SELECT * FROM flashcards 
            WHERE question LIKE ? OR answer LIKE ?
            ORDER BY created_at DESC
            """,
            f"%{query}%",
            f"%{query}%",
        )
        return render_template(
            "flashcards.html", flashcards=flashcards, search_query=query
        )
    except Exception as e:
        flash(f"Error during search: {e}", "error")
        return redirect(url_for("flashcards.flashcards"))


@flashcards_blueprint.route("/create_deck", methods=["GET"])
def create_deck():
    # Fetch available notes for the "Generate Deck from Notes" option
    notes = db.execute("SELECT id, title FROM notes ORDER BY created_at DESC")
    return render_template("create_deck.html", current_route="flashcards", notes=notes)


@flashcards_blueprint.route("/create_deck_plain", methods=["POST"])
def create_deck_plain():
    """
    Handle creation of a plain deck (no text or note-based generation).
    """
    title = request.form.get("title")
    description = request.form.get("description")

    if not title:
        flash("Deck title is required!", "error")
        return redirect(url_for("flashcards.create_deck"))

    try:
        db.execute(
            """
            INSERT INTO decks (title, description, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            title,
            description,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        flash("Plain deck created successfully!", "success")
    except Exception as e:
        flash(f"Error creating plain deck: {e}", "error")

    return redirect(url_for("flashcards.flashcards"))


@flashcards_blueprint.route("/generate_deck", methods=["POST"])
def generate_deck():
    input_text = request.form.get("input_text")

    if not input_text:
        flash("Text input field is required.", "error")
        return redirect(url_for("flashcards.create_deck"))

    num_clusters = request.form.get("num_clusters", type=int, default=5)
    title = get_title(input_text)
    ic(title)
    description = generate_description(input_text)

    try:
        # Create a new deck
        db.execute(
            """
            INSERT INTO decks (title, description, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        """,
            title,
            description,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        result_deck_id = db.execute("SELECT last_insert_rowid()")
        deck_id = result_deck_id[0]["last_insert_rowid()"]

        ic(deck_id)

        # Generate flashcards from the input text
        sentences = input_text.split(".")
        generated_flashcards = generate_flashcards(sentences, num_clusters)

        # Add generated flashcards to the deck
        for cluster in generated_flashcards:
            question = f"{cluster[0]}"
            answer = " ".join(cluster)
            db.execute(
                """
                INSERT INTO flashcards (deck_id, note_id, question, answer, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                deck_id,
                None,
                question,
                answer,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

        flash(
            f"Deck '{title}' created successfully with {len(generated_flashcards)} flashcards.",
            "success",
        )
        return redirect(url_for("flashcards.flashcards"))
    except Exception as e:
        flash(f"Error generating deck: {e}", "error")
        return redirect(url_for("flashcards.create_deck"))


@flashcards_blueprint.route("/generate_deck_automatic", methods=["POST"])
def generate_deck_automatic():
    """
    Automatically generate flashcards for a deck using the content of selected notes (by note_ids).
    """
    note_ids = request.form.getlist("note_ids")  # Get the list of note IDs

    if not note_ids:
        flash("Please select at least one note.", "error")
        return redirect(url_for("flashcards.flashcards"))

    try:
        # Create a new deck for the selected notes
        # Combine the content of all selected notes into a single text input for description generation
        combined_content = ""
        for note_id in note_ids:
            note = db.execute("SELECT title, content FROM notes WHERE id = ?", note_id)
            if not note:
                flash(f"Note with ID {note_id} not found.", "error")
                continue
            note[0]["title"]  # Fetch the title from the note
            note_content = note[0]["content"]
            combined_content += note_content + "\n"  # Append note content

        # Use the first note's title as the deck title (or modify logic as needed)
        deck_title = note[0]["title"] if note else "Untitled Deck"
        deck_description = generate_description(
            combined_content
        )  # Generate description using combined content

        db.execute(
            """
            INSERT INTO decks (title, description, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        """,
            deck_title,
            deck_description,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        # Retrieve the deck ID
        result_deck_id = db.execute("SELECT last_insert_rowid()")
        deck_id = result_deck_id[0]["last_insert_rowid()"]

        # Loop over each note_id and generate flashcards
        for note_id in note_ids:
            note = db.execute("SELECT title, content FROM notes WHERE id = ?", note_id)
            if not note:
                flash(f"Note with ID {note_id} not found.", "error")
                ic(f"Note with ID {note_id} not found.", "error")
                continue

            note_content = note[0]["content"]  # Fetch the content

            # Generate flashcards based on note content
            sentences = note_content.split(".")
            generated_flashcards = generate_flashcards(sentences, num_clusters=5)

            for cluster in generated_flashcards:
                question = f"{cluster[0]}"  # Simplified question
                answer = " ".join(cluster)  # Concatenate cluster details as the answer
                db.execute(
                    """
                    INSERT INTO flashcards (deck_id, note_id, question, answer, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    deck_id,  # Link to the newly created deck
                    note_id,  # Link to the specific note
                    question,
                    answer,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )

        flash(
            f"Flashcards generated successfully and all linked to deck {deck_id}.",
            "success",
        )
        ic(
            f"Flashcards generated successfully and all linked to deck {deck_id}.",
            "success",
        )
    except Exception as e:
        flash(f"Error generating flashcards: {e}", "error")
        ic(f"Error generating flashcards: {e}", "error")

    return redirect(url_for("flashcards.flashcards"))


@flashcards_blueprint.route("/review", methods=["GET"])
def review():
    """
    Review mode for students: fetch all flashcards for the selected deck
    and let the frontend handle navigation and display.
    """
    selected_deck_id = request.args.get("deck_id", "all")

    # Fetch flashcards from the database
    if selected_deck_id == "all":
        flashcards = db.execute("SELECT * FROM flashcards ORDER BY created_at DESC")
    else:
        flashcards = db.execute(
            "SELECT * FROM flashcards WHERE deck_id = ? ORDER BY created_at DESC",
            selected_deck_id,
        )

    if not flashcards:
        flash("No flashcards available for review.", "info")
        return redirect(url_for("flashcards.flashcards"))

    # Render the review deck template with all flashcards
    return render_template(
        "review_deck.html", flashcards=flashcards, deck_id=selected_deck_id
    )
