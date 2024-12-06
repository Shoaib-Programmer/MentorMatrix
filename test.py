from models import db
from datetime import datetime
from icecream import ic

deck_id = 1
note_id = 1
question = 'what is hello?'
answer = 'a greeting'

try:
    db.execute(
        """
        INSERT INTO flashcards (title, description, created_at, updated)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        'general',
        'Just for testing the db!',
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
except Exception as e:
    ic(f"Error adding flashcard: {e}", "error")

try:
    db.execute(
        """
        INSERT INTO flashcards (deck_id, note_id, question, answer, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        deck_id,
        note_id,
        question,
        answer,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
except Exception as e:
    ic(f"Error adding flashcard: {e}", "error")