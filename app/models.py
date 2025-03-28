from cs50 import SQL

# Connect to the development database.
db = SQL("sqlite:///instance/dev.db")


def init_db():
    """
    Initializes the database by creating the necessary tables and indexes.

    This function sets up the following tables:
        - `users`: our own authentication table (replacing Auth0).
        - `transcripts`, `notes`, `files`, `quizzes`, `quiz_questions`,
          `decks`, `flashcards`, `quiz_results`, and `podcasts` with UUID primary keys.
    """
    global db  # Declare db as global to modify the global object

    # Create a "users" table for our custom authentication.
    db.execute(
        """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                salt TEXT,
                confirmed BOOLEAN NOT NULL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );"""
    )

    # The following tables use a default UUID (128-bit) generated by SQLite.
    db.execute("""CREATE TABLE IF NOT EXISTS transcripts (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );""")

    db.execute("""CREATE TABLE IF NOT EXISTS notes (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    transcript_id TEXT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    user_id TEXT NOT NULL DEFAULT '',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE
                );""")

    db.execute("""CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transcript_id TEXT NOT NULL,
                    file_type TEXT CHECK(file_type IN ('audio', 'youtube', 'pdf')) NOT NULL,
                    name TEXT NOT NULL,
                    metadata TEXT,
                    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE
                );""")

    db.execute("""CREATE TABLE IF NOT EXISTS quizzes (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    transcript_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE
                );""")

    db.execute("""CREATE TABLE IF NOT EXISTS quiz_questions (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    quiz_id TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    question_type TEXT CHECK(question_type IN ('open_ended', 'multiple_choice')) NOT NULL,
                    options TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
                );""")

    db.execute("""CREATE TABLE IF NOT EXISTS decks (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    title TEXT NOT NULL,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );""")

    db.execute("""CREATE TABLE IF NOT EXISTS flashcards (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    deck_id TEXT NOT NULL,
                    note_id TEXT,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (deck_id) REFERENCES decks(id) ON DELETE CASCADE,
                    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
                );""")

    db.execute("""CREATE TABLE IF NOT EXISTS quiz_results (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    quiz_id TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    attempted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
                );""")

    db.execute("""CREATE TABLE IF NOT EXISTS podcasts (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    note_id TEXT,
                    content TEXT NOT NULL,
                    path TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
                );""")

    # Create indexes for faster lookups
    db.execute("CREATE INDEX IF NOT EXISTS idx_transcript_id ON notes (transcript_id);")
    db.execute(
        "CREATE INDEX IF NOT EXISTS idx_file_transcript_id ON files (transcript_id);"
    )
    db.execute(
        "CREATE INDEX IF NOT EXISTS idx_quiz_transcript_id ON quizzes (transcript_id);"
    )
    db.execute(
        "CREATE INDEX IF NOT EXISTS idx_quiz_question_quiz_id ON quiz_questions (quiz_id);"
    )
    db.execute("CREATE INDEX IF NOT EXISTS idx_deck_title ON decks (title);")
    db.execute(
        "CREATE INDEX IF NOT EXISTS idx_flashcard_deck_id ON flashcards (deck_id);"
    )

    # Create index for faster user-based queries
    db.execute("CREATE INDEX IF NOT EXISTS idx_notes_user_id ON notes (user_id);")


def get_user_by_email(email: str):
    """Fetches a user (or users) from the database by email."""
    rows = db.execute("SELECT * FROM users WHERE email = ?", email)
    return rows


def get_user_by_username(username: str):
    """Fetches a user (or users) from the database by username."""
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)
    return rows


def create_standard_user(
    username: str, email: str, hashed_password: str, confirmed: bool, salt: str
):
    """
    Creates a new user with the provided details.

    Args:
        username (str): The user's username.
        email (str): The user's email address.
        hashed_password (str): The hashed password.
        confirmed (bool): Whether the user's email is confirmed.
        salt (str): The salt used (if applicable).
    """
    db.execute(
        "INSERT INTO users (username, email, password, salt, confirmed) VALUES (?, ?, ?, ?, ?)",
        username,
        email,
        hashed_password,
        salt,
        int(confirmed),
    )


def update_user_confirmation_status(email: str, confirmed: bool):
    """
    Updates the confirmation status for a user identified by email.

    Args:
        email (str): The user's email address.
        confirmed (bool): The new confirmation status.
    """
    db.execute("UPDATE users SET confirmed = ? WHERE email = ?", int(confirmed), email)


def update_user_password(email: str, hashed_password: str, salt: str):
    """
    Updates the user's password in the database.

    Args:
        email (str): The user's email address.
        hashed_password (str): The new hashed password.
        salt (str): The new salt value.
    """
    db.execute(
        "UPDATE users SET password = ?, salt = ? WHERE email = ?",
        hashed_password,
        salt,
        email,
    )


def get_user_by_oauth(provider: str, oauth_id: str):
    """
    Stub function for OAuth users.
    Since we're rolling out our own auth, this can return None or be implemented as needed.
    """
    return None


if __name__ == "__main__":
    init_db()  # For debugging: initialize the database when running this module directly.
