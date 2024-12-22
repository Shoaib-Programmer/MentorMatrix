from cs50 import SQL


db = SQL("sqlite:///dev.db")

def init_db():
    """
    Initializes the database by creating the necessary tables and indexes.

    This function sets up the following tables in the database:
        - `transcripts`: Stores the main transcript data with title, content, and timestamps.
        - `notes`: Stores notes related to transcripts, with a foreign key reference to the `transcripts` table.
        - `files`: Stores associated files (e.g., audio, YouTube, PDFs) linked to transcripts, with metadata.
        - `quizzes`: Stores quizzes related to transcripts.
        - `quiz_questions`: Stores questions for each quiz, with options for multiple-choice questions.
        - `quiz_results`: Stores quiz results, including the quiz ID, user ID (if applicable), score, and timestamp.
        - `decks`: Stores flashcard decks.
        - `flashcards`: Stores individual flashcards, linked to both decks and notes.

    Additionally, the function creates indexes on key columns (e.g., transcript ID, quiz ID, deck title) to improve query performance.
    """

    
    global db  # Declare db as global to modify the global object

    # Create the necessary tables
    db.execute('''CREATE TABLE IF NOT EXISTS transcripts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP);''')

    db.execute('''CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transcript_id INTEGER,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE);''')

    db.execute('''CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transcript_id INTEGER NOT NULL,
                    file_type TEXT CHECK(file_type IN ('audio', 'youtube', 'pdf')) NOT NULL,
                    name TEXT NOT NULL,
                    metadata TEXT,  -- JSON or additional metadata as text
                    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE);''')


    db.execute('''CREATE TABLE IF NOT EXISTS quizzes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transcript_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE);''')

    db.execute('''CREATE TABLE IF NOT EXISTS quiz_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quiz_id INTEGER NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    question_type TEXT CHECK(question_type IN ('open_ended', 'multiple_choice')) NOT NULL,
                    options TEXT,  -- Store multiple-choice options as a JSON string
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE);''')

    # Flashcards Table with a reference to Decks
    db.execute('''CREATE TABLE IF NOT EXISTS decks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP);''')

    db.execute('''CREATE TABLE IF NOT EXISTS flashcards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    deck_id INTEGER NOT NULL,
                    note_id INTEGER,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (deck_id) REFERENCES decks(id) ON DELETE CASCADE,
                    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE);''')
    
    db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                -- user_id INTEGER, Optional, if multi-user functionality exists
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                attempted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE);''')

    db.execute('''CREATE TABLE IF NOT EXISTS podcasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note_id INTEGER,
                content TEXT NOT NULL,
                path TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE);''')


    # Create indexes for faster lookups
    db.execute('CREATE INDEX IF NOT EXISTS idx_transcript_id ON notes (transcript_id);')
    db.execute('CREATE INDEX IF NOT EXISTS idx_file_transcript_id ON files (transcript_id);')
    db.execute('CREATE INDEX IF NOT EXISTS idx_quiz_transcript_id ON quizzes (transcript_id);')
    db.execute('CREATE INDEX IF NOT EXISTS idx_quiz_question_quiz_id ON quiz_questions (quiz_id);')
    db.execute('CREATE INDEX IF NOT EXISTS idx_deck_title ON decks (title);')
    db.execute('CREATE INDEX IF NOT EXISTS idx_flashcard_deck_id ON flashcards (deck_id);')


if __name__ == "__main__":
    init_db() # This is just a debugging step
