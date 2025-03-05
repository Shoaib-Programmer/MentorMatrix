This is an app with a backend in flask and a frontend made with HTML, CSS and JS, with a little tailwind sprinkled here and there. It does not use any JS framework.

The remote is at github.com/Shoaib-Programmer/MentorMatrix

Here is the structure of the app:
.
├── LICENSE
├── MentorMatrix.docx
├── MentorMatrix.md
├── MentorMatrix.pdf
├── README.md
├── app
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── forms.py
│   ├── middleware.py
│   ├── models.py
│   ├── notes
│   │   ├── AI
│   │   │   ├── __init__.py
│   │   │   ├── answer_open.py
│   │   │   ├── chatbot.py
│   │   │   ├── description.py
│   │   │   ├── fill_in_the_blank.py
│   │   │   ├── flashcards.py
│   │   │   ├── get_title_for_context.py
│   │   │   ├── multiple_choice.py
│   │   │   ├── podcast.py
│   │   │   ├── question_generation.py
│   │   │   ├── quiz.py
│   │   │   ├── semantic_compare.py
│   │   │   ├── stopwords.py
│   │   │   └── summarize.py
│   │   ├── __init__.py
│   │   └── transcription
│   │       ├── __init__.py
│   │       ├── audio
│   │       │   ├── __init__.py
│   │       │   └── audio_analysis.py
│   │       ├── text
│   │       │   └── pdf.py
│   │       ├── util.py
│   │       ├── video
│   │       │   ├── __init__.py
│   │       │   └── video_analysis.py
│   │       ├── video_transcribe.py
│   │       ├── youtube.py
│   │       └── youtube_id.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── chatbot.py
│   │   ├── dashboard.py
│   │   ├── errors.py
│   │   ├── flashcards.py
│   │   ├── notes.py
│   │   ├── podcast.py
│   │   ├── quiz.py
│   │   └── transcribe.py
│   ├── src
│   │   └── styles
│   │       └── tailwind.css
│   ├── static
│   │   ├── css
│   │   │   ├── base.css
│   │   │   ├── chatbot.css
│   │   │   ├── dashboard
│   │   │   │   └── dashboard.css
│   │   │   ├── flashcards.css
│   │   │   ├── light.css
│   │   │   ├── notes.css
│   │   │   ├── popup.css
│   │   │   ├── quiz.css
│   │   │   ├── settings.css
│   │   │   ├── tailwind.css
│   │   │   ├── transcript.css
│   │   │   ├── view_note.css
│   │   │   └── view_transcript.css
│   │   ├── dist
│   │   ├── images
│   │   │   ├── MentorMatrix_logo.png
│   │   │   ├── angle-left.svg
│   │   │   ├── angle-right.svg
│   │   │   ├── download.svg
│   │   │   ├── edit.svg
│   │   │   ├── favicon.ico
│   │   │   ├── hamburger.svg
│   │   │   ├── mic.svg
│   │   │   ├── mr_grumpy.png
│   │   │   ├── mr_spooky.png
│   │   │   ├── sidebar-toggle.svg
│   │   │   ├── three_dots.svg
│   │   │   └── upload.svg
│   │   └── js
│   │       ├── chatbot.js
│   │       ├── dashboard
│   │       │   └── popup.js
│   │       ├── flashcards.js
│   │       ├── notes.js
│   │       ├── progress.js
│   │       ├── quiz.js
│   │       ├── settings.js
│   │       ├── transcript.js
│   │       └── util.js
│   ├── templates
│   │   ├── 404.html
│   │   ├── 500.html
│   │   ├── base.html
│   │   ├── chatbot.html
│   │   ├── create_deck.html
│   │   ├── dashboard.html
│   │   ├── edit_flashcard.html
│   │   ├── email
│   │   │   └── confirm.html
│   │   ├── flashcards.html
│   │   ├── generate_podcast.html
│   │   ├── layout.html
│   │   ├── login.html
│   │   ├── notes.html
│   │   ├── podcast.html
│   │   ├── pricing.html
│   │   ├── quiz.html
│   │   ├── quiz_question.html
│   │   ├── review_deck.html
│   │   ├── settings.html
│   │   ├── transcript.html
│   │   ├── view_note.html
│   │   └── view_transcript.html
├── instance
│   ├── dev.db
│   └── flask_session
│       ...
├── package.json
├── pnpm-lock.yaml
├── podcasts
├── postcss.config.js
├── requirements.txt
├── run.py
├── setup.sh
├── tailwind.config.js
├── uploads
│   ...
└── vite.config.js

38 directories, 186 files

This app uses Clerk for auth. It also uses an SQLite Database.
Here is the schema for your reference:

CREATE TABLE transcripts (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
CREATE TABLE notes (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    transcript_id TEXT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE
                );
CREATE TABLE files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transcript_id TEXT NOT NULL,
                    file_type TEXT CHECK(file_type IN ('audio', 'youtube', 'pdf')) NOT NULL,
                    name TEXT NOT NULL,
                    metadata TEXT,
                    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE quizzes (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    transcript_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE
                );
CREATE TABLE quiz_questions (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    quiz_id TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    question_type TEXT CHECK(question_type IN ('open_ended', 'multiple_choice')) NOT NULL,
                    options TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
                );
CREATE TABLE decks (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    title TEXT NOT NULL,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
CREATE TABLE flashcards (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    deck_id TEXT NOT NULL,
                    note_id TEXT,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (deck_id) REFERENCES decks(id) ON DELETE CASCADE,
                    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
                );
CREATE TABLE quiz_results (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    quiz_id TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    attempted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
                );
CREATE TABLE podcasts (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    note_id TEXT,
                    content TEXT NOT NULL,
                    path TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
                );
CREATE INDEX idx_transcript_id ON notes (transcript_id);
CREATE INDEX idx_file_transcript_id ON files (transcript_id);
CREATE INDEX idx_quiz_transcript_id ON quizzes (transcript_id);
CREATE INDEX idx_quiz_question_quiz_id ON quiz_questions (quiz_id);
CREATE INDEX idx_deck_title ON decks (title);
CREATE INDEX idx_flashcard_deck_id ON flashcards (deck_id);


Secrets are stored in .env.

The notes folder is a services folder which acts like an API for the project's tasks, like summarizing and creating flashcards.

This project uses local ollama for AI services. We are looking forward to integrate OpenAI or
DeekSeek's API.
