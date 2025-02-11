from flask import Flask, render_template  # type: ignore
from flask_session import Session  # type: ignore
from flask_mail import Mail  # type: ignore

from app.config import Config, DevelopmentConfig  # Import the config dictionary
from app.routes import (
    dashboard_blueprint,
    notes_blueprint,
    transcribe_blueprint,
    chatbot_blueprint,
    quiz_blueprint,
    flashcards_blueprint,
    podcast_blueprint,
    auth_blueprint,
    error_blueprint,
)
from app.models import init_db

# Initialize the Flask app
app = Flask(__name__)


# Load the appropriate configuration based on the environment
app.config.from_object(DevelopmentConfig)

# Initialize the app's folders (i.e., create the directories if they don't exist)
Config.init_app(app)


# Flask-Session Configuration
app.config["SESSION_TYPE"] = (
    "filesystem"  # Stores session data in the server file system
)
app.config["SESSION_PERMANENT"] = True  # Make sessions permanent
app.config["PERMANENT_SESSION_LIFETIME"] = 3600  # Session lifetime in seconds (1 hour)
Session(app)  # Initialize Flask-Session

# Mail configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = "authsimple.eshaan@gmail.com"
app.config["MAIL_PASSWORD"] = "kuqb lgto jtod lfjm"
app.config["MAIL_DEFAULT_SENDER"] = "authsimple.eshaan@gmail.com"

mail = Mail(app)

# Initialize SQLite database (this will create the tables)
init_db()

# Register blueprints for different routes
with app.app_context():
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(podcast_blueprint)
    app.register_blueprint(notes_blueprint)
    app.register_blueprint(transcribe_blueprint)
    app.register_blueprint(chatbot_blueprint)
    app.register_blueprint(quiz_blueprint)
    app.register_blueprint(flashcards_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(error_blueprint)

# Miscellaneous routes for now


@app.route("/settings")
def settings():
    return render_template("settings.html", current_route="settings")


@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


if __name__ == "__main__":
    app.run(debug=True, host="::", port=5000)
