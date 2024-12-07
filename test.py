from models import db
from datetime import datetime
from icecream import ic

try:
    # First, insert into the decks table
    result = db.execute(
        """
        INSERT INTO decks (title, description, created_at, updated_at)
        VALUES (?, ?, ?, ?)
        """,
        'Sample Deck',  # Example deck title
        'A sample deck for flashcards',  # Example deck description
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    # Check if insertion was successful (result should be > 0 if rows are inserted)
    if result == 0:
        ic("Deck insertion failed. No rows inserted.", "error")
    else:
        # Now, retrieve the last inserted deck_id using a SELECT query
        result = db.execute("SELECT last_insert_rowid()")
        ic(result)
        deck_id = result[0]['last_insert_rowid()']
        ic(deck_id)
        
        # Check if deck_id is valid (non-zero)
        if deck_id == 0:
            ic("Failed to retrieve deck_id. It is 0.", "error")
        else:
            ic(f"Deck created with ID: {deck_id}")

            # Now insert into the flashcards table using the deck_id
            db.execute(
                """
                INSERT INTO flashcards (deck_id, question, answer, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                deck_id,
                'What is hello?',
                'A greeting',
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            ic("Flashcard successfully inserted.")

except Exception as e:
    ic(f"Error adding flashcard: {e}", "error")
