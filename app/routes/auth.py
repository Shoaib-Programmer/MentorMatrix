from flask import Blueprint, render_template , redirect, session, request # type: ignore
from app.middleware import verify_clerk_token

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/login')
def login():
    # Attempt to retrieve the token from the Authorization header
    auth_header = request.headers.get("Authorization")
    token = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    else:
        # Fallback: get the token from the session
        token = session.get("token")
    
    # If a token is present and valid, redirect to home
    if token and verify_clerk_token(token):
        return redirect('/')
    
    # Otherwise, show the login page
    return render_template('login.html')


@auth_blueprint.route('/register')
def register():
    return redirect('https://pleasant-humpback-47.accounts.dev/sign-up?redirect_url=http%3A%2F%2F127.0.0.1%3A5000%2F')

def handle_successful_login(token):
    """Store the JWT token in the session and redirect to the home page."""
    session['token'] = token  # Store token securely in the session
    return redirect('/')

@auth_blueprint.route('/callback')
def auth_callback():
    # Use __clerk_handshake as it appears to be a valid JWT
    token = request.args.get("__clerk_handshake")
    print("Received token:", token)  # For debugging
    
    if not token:
        return redirect('/auth/login')
    
    session['token'] = token
    return redirect('/dashboard')

