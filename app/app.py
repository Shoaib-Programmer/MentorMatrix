from flask import Flask, render_template, g # type: ignore
from flask_session import Session
from flask_mail import Mail # type: ignore
from flask_wtf.csrf import CSRFProtect, generate_csrf # type: ignore

# Import your configuration and blueprints
from app.config import DevelopmentConfig  # or use config["development"] from the mapping if preferred
from app.routes import (
    dashboard_blueprint,  # noqa: F401
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

# Create the Flask application
app = Flask(__name__, static_folder='static', template_folder='templates')

# Load the configuration (using DevelopmentConfig as an example)
app.config.from_object(DevelopmentConfig)

# Initialize app-specific settings (e.g. creating folders)
DevelopmentConfig.init_app(app)

# Set up CSRF protection and make the CSRF token available in templates
csrf = CSRFProtect(app)
app.jinja_env.globals["csrf_token"] = generate_csrf
app.context_processor(lambda: {"csrf_token": generate_csrf})

# Initialize session and mail extensions (their settings are loaded via config)
Session(app)
mail = Mail(app)

# Initialize the database (this creates the necessary tables)
init_db()

@app.context_processor
def inject_clerk_config():
    return dict(current_user=g.get('clerk_payload'))


# Register blueprints within an application context
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

# Miscellaneous routes
@app.route("/settings")
def settings():
    return render_template("settings.html", current_route="settings")

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


if __name__ == "__main__":
    app.run(debug=True, host="::", port=5000)
