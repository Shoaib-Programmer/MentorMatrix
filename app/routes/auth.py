import os
import logging
from urllib.parse import urlencode
from flask import (
    Blueprint,
    redirect,
    url_for,
    session,
    request,
    render_template_string,
)
from auth0.authentication import GetToken  # Auth0 Python SDK for token exchange

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

# Configuration (ensure these environment variables are set)
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")  # e.g., 'my-domain.us.auth0.com'
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
# AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")
AUTH0_CALLBACK_URL = "https://a88e-152-59-195-71.ngrok-free.app/auth/callback"
AUTH0_SCOPE = "openid profile email"
# AUTH0_AUDIENCE = "https://dev-nlswp33on5rnohcr.us.auth0.com/api/v2"


@auth_blueprint.route("/login")
def login():
    # Clear any existing session
    session.clear()
    # Generate a state parameter for CSRF protection
    state = os.urandom(16).hex()
    session["oauth_state"] = state

    # Build the Auth0 authorization URL
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": AUTH0_SCOPE,
        "state": state,
        # "audience": AUTH0_AUDIENCE,  # This tells Auth0 to issue an access token with that audience.
    }

    auth_url = f"https://{AUTH0_DOMAIN}/authorize?" + urlencode(params)
    return redirect(auth_url)


@auth_blueprint.route("/callback")
def auth_callback():
    # Validate state parameter
    received_state = request.args.get("state")
    expected_state = session.get("oauth_state")
    if received_state is None or received_state != expected_state:
        logging.debug(f"Received state: {received_state}, expected: {expected_state}")
        logging.warning("Invalid state parameter")
        return redirect("/auth/login")

    # Retrieve the authorization code from query parameters
    code = request.args.get("code")
    if not code:
        logging.error("No code parameter found in callback")
        return render_template_string(
            "<h1>Authentication Error</h1><p>No authorization code provided.</p>"
        ), 400

    try:
        # Exchange the authorization code for tokens using Auth0's GetToken
        get_token = GetToken(
            AUTH0_DOMAIN, AUTH0_CLIENT_ID, client_secret=AUTH0_CLIENT_SECRET
        )
        token_response = get_token.authorization_code(
            redirect_uri=AUTH0_CALLBACK_URL, code=code
        )
        # token_response should contain "id_token" and "access_token"
        id_token = token_response.get("id_token")
        if not id_token:
            logging.error("No id_token in token response")
            return render_template_string(
                "<h1>Authentication Error</h1><p>No ID token received.</p>"
            ), 400
        # Store the ID token in session for subsequent authentication (middleware will verify it)
        session["auth0_id_token"] = id_token
        session.modified = True
        return redirect("/dashboard")
    except Exception as e:
        logging.error(f"Error exchanging code for tokens: {e}")
        return redirect("/auth/login")


@auth_blueprint.route("/register")
def register():
    # Redirect to Auth0's Universal Login sign-up page.
    params = {
        "screen_hint": "signup",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": AUTH0_SCOPE,
        "state": os.urandom(16).hex(),
    }
    signup_url = f"https://{AUTH0_DOMAIN}/authorize?" + urlencode(params)
    return redirect(signup_url)


@auth_blueprint.route("/logout")
def logout():
    # Clear the local session
    session.clear()

    # Build the Auth0 logout URL
    params = {
        "client_id": AUTH0_CLIENT_ID,
        "returnTo": url_for(
            "dashboard.index", _external=True
        ),  # Change "home" to your desired post-logout endpoint
    }
    logout_url = f"https://{AUTH0_DOMAIN}/v2/logout?" + urlencode(params)
    return redirect(logout_url)
