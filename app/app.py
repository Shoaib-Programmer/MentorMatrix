from os import environ as env

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

from flask import Flask, render_template
from flask_session import Session
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect, generate_csrf  # type: ignore

# Import your configuration and blueprints
from app.config import (
    DevelopmentConfig,
)  # or use config["development"] from the mapping if preferred
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
from app.middleware import requires_auth

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Create the Flask application
app = Flask(__name__, static_folder="static", template_folder="templates")

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

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{env.get('AUTH0_DOMAIN')}/.well-known/openid-configuration",
)

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
@requires_auth
def settings():
    return render_template("settings.html", current_route="settings")


@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


if __name__ == "__main__":
    app.run(debug=True, host="::", port=5000)
