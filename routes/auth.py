from flask import (  # type: ignore
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    request,
    current_app,
)
from flask_session import Session  # type: ignore
from flask_mail import Mail, Message  # type: ignore

from dotenv import load_dotenv  # type: ignore

from itsdangerous import URLSafeTimedSerializer  # type: ignore
from authlib.integrations.flask_client import OAuth  # type: ignore
from icecream import ic  # type: ignore
import uuid
import os

from utils.password import hash_password, verify_password
from models import (
    get_user_by_email,
    create_standard_user,
    get_user_by_username,
    get_user_by_oauth,
    create_oauth_user,
    update_user_confirmation_status,
)

from forms import LoginForm, RegisterForm

load_dotenv()

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = os.environ.get("GOOGLE_DISCOVERY_URL")

auth_blueprint = Blueprint("auth", __name__)


# Load configuration
current_app.secret_key = "your-secret-key"

# Configure OAuth
oauth = OAuth(current_app)
google = oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"prompt": "consent", "access_type": "offline"},
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    client_kwargs={
        "scope": "openid email profile",
        "token_endpoint_auth_method": "client_secret_post",
        "state": True,
    },
    server_metadata_url=GOOGLE_DISCOVERY_URL,
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
    issuer="https://accounts.google.com",
)

# Flask-Session Configuration
current_app.config["SESSION_TYPE"] = (
    "filesystem"  # Stores session data in the server file system
)
current_app.config["SESSION_PERMANENT"] = True  # Make sessions permanent
current_app.config["PERMANENT_SESSION_LIFETIME"] = (
    3600  # Session lifetime in seconds (1 hour)
)
Session(current_app)  # Initialize Flask-Session

current_app.config["MAIL_SERVER"] = "smtp.gmail.com"
current_app.config["MAIL_PORT"] = 587
current_app.config["MAIL_USE_TLS"] = True
current_app.config["MAIL_USE_SSL"] = False
current_app.config["MAIL_USERNAME"] = "authsimple.eshaan@gmail.com"
current_app.config["MAIL_PASSWORD"] = "kuqb lgto jtod lfjm"
current_app.config["MAIL_DEFAULT_SENDER"] = "authsimple.eshaan@gmail.com"

mail = Mail(current_app)

s = URLSafeTimedSerializer(current_app.secret_key)


def generate_confirmation_token(email):
    return s.dumps(email, salt=current_app.secret_key)


def confirm_token(token, expiration=3600):
    try:
        email = s.loads(token, salt=current_app.secret_key, max_age=expiration)
    except Exception:
        return False
    return email


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Hash the password
        hashed_password, salt = hash_password(password)  # Get hashed password and salt

        # Check if the email is already registered
        existing_user = get_user_by_email(email)
        if existing_user:
            flash("Email is already registered!", "danger")
            return redirect(url_for("register"))

        # Create a new user but set confirmed to False initially
        create_standard_user(
            username, email, hashed_password, confirmed=False, salt=salt
        )  # Store salt

        # Generate the token for email confirmation
        token = generate_confirmation_token(email)
        confirm_url = url_for("confirm_email", token=token, _external=True)
        html = render_template("email/confirm.html", confirm_url=confirm_url)

        # Send the confirmation email
        msg = Message("Please confirm your email", recipients=[email])
        msg.html = html
        mail.send(msg)

        flash(
            "Registration successful! A confirmation email has been sent. Please confirm your email to complete registration.",
            "success",
        )
        return redirect(url_for("index"))

    return render_template("register.html", form=form)


@auth_blueprint.route("/confirm/<token>")
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        return redirect(url_for("index"))

    user = get_user_by_email(email)
    if not user:
        flash("Account not found.", "danger")
        return redirect(url_for("index"))

    if user[0]["confirmed"]:
        flash("Account already confirmed. Please log in.", "info")
    else:
        update_user_confirmation_status(email, True)
        flash("You have confirmed your account. Thanks!", "success")

    return redirect(url_for("login"))


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if "user_id" in session:
        flash("You are already logged in.", "info")
        return redirect(url_for("index"))

    if form.validate_on_submit():
        username_or_email = form.username_or_email.data
        password = form.password.data

        # Try to get user by email first
        user = get_user_by_email(username_or_email)
        if not user:
            user = get_user_by_username(username_or_email)
            if not user:
                flash("Invalid username/email or password!", "danger")
                return redirect(url_for("login"))

        # Check if user is an OAuth user
        if user[0]["password"] in (None, "oauth"):
            flash("Please log in using Google.", "warning")
            return redirect(url_for("login"))

        # Verify password
        salt = user[0]["salt"]  # Retrieve the stored salt
        if not verify_password(password, user[0]["password"], salt):  # Pass the salt
            flash("Invalid username/email or password!", "danger")
            return redirect(url_for("login"))

        session["user_id"] = user[0]["id"]
        session["username"] = user[0]["username"]
        flash(f"Welcome back, {user[0]['username']}!", "success")
        return redirect(url_for("index"))

    return render_template("login.html", form=form)


@auth_blueprint.route("/auth/google")
def google_login():
    redirect_uri = url_for("google_callback", _external=True)
    # Generate secure state and nonce tokens
    state = session.get("state") or str(uuid.uuid4())
    nonce = session.get("nonce") or str(uuid.uuid4())
    session["state"] = state
    session["nonce"] = nonce
    return google.authorize_redirect(redirect_uri, state=state, nonce=nonce)


@auth_blueprint.route("/auth/google/callback")
def google_callback():
    try:
        # Verify state parameter
        if "state" not in request.args or request.args.get("state") != session.get(
            "state"
        ):
            flash("Invalid state parameter. Possible CSRF attack.", "danger")
            return redirect(url_for("login"))

        # Clear the state from session
        session.pop("state", None)

        token = google.authorize_access_token()
        ic(token)
        if not token:
            flash("Google login failed. Please try again.", "danger")
            return redirect(url_for("login"))

        # Verify the token
        if "id_token" not in token:
            flash("Invalid token received from Google.", "danger")
            return redirect(url_for("login"))

        # Get and validate user info from Google
        user_info = google.parse_id_token(
            token,
            nonce=session.get("nonce"),
            claims_options={
                "iss": {"values": ["https://accounts.google.com"], "essential": True},
                "aud": {"values": [GOOGLE_CLIENT_ID], "essential": True},
            },
        )
        # Clear the nonce from session
        session.pop("nonce", None)
        if not user_info:
            flash("Failed to get user information from Google.", "danger")
            return redirect(url_for("login"))

    except Exception as e:
        flash(f"An error occurred during Google login: {str(e)}", "danger")
        return redirect(url_for("login"))

    # Check if user exists in our database
    google_id = user_info.get("sub")
    if not google_id:
        flash("Failed to get Google user ID.", "danger")
        return redirect(url_for("login"))

    user = get_user_by_oauth("google", google_id)

    # Extracting the amail
    email = user_info.get("email")
    if not email:
        flash("Failed to get Google user email.", "danger")
        return redirect(url_for("login"))

    if not user:
        create_oauth_user(email, "google", google_id)
        user = get_user_by_oauth("google", google_id)

    # Extracting the username
    username = (
        user_info.get("name") or user_info.get("given_name") or email.split("@")[0]
    )

    # Log the user in
    session["user_id"] = user[0]["id"]
    session["username"] = username
    flash(f"Welcome, {session['username']}!", "success")
    return redirect(url_for("index"))


@auth_blueprint.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))
