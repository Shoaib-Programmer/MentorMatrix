from flask import Blueprint, redirect, session, request, url_for, render_template_string # type: ignore
import os
import logging

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/login')
def login():
    # Clear any existing session
    session.clear()
    
    # Build callback URL (using HTTPS in production, HTTP otherwise)
    is_production = os.getenv('FLASK_ENV') == 'production'
    callback_url = url_for('auth.auth_callback', _external=True, _scheme='https' if is_production else 'http')
    
    clerk_frontend_api = os.environ.get('CLERK_FRONTEND_API')
    if not clerk_frontend_api:
        logging.error("Missing CLERK_FRONTEND_API environment variable")
        return "Configuration error", 500
        
    # Generate a state parameter to help prevent CSRF
    state = os.urandom(16).hex()
    session['oauth_state'] = state
    
    # Redirect to Clerk's sign-in page
    return redirect(f"{clerk_frontend_api}/sign-in?redirect_url={callback_url}&state={state}")

@auth_blueprint.route('/register')
def register():
    return redirect('https://pleasant-humpback-47.accounts.dev/sign-up')

@auth_blueprint.route('/callback')
def auth_callback():
    # Validate state parameter
    try:
        # Retrieve state from the request, if available.
        received_state = request.args.get('state')
        expected_state = session.get('oauth_state')

        if received_state is not None:
            logging.debug(f"Received state: {received_state}")
            if received_state != expected_state:
                logging.warning('Invalid state parameter')
                return redirect('/auth/login')
        else:
            logging.debug("No state parameter received from Clerk; skipping state validation.")
        
        # Retrieve the session token from __clerk_db_jwt
        token = request.args.get('__clerk_db_jwt')
        if not token:
            logging.warning("No token received in callback via __clerk_db_jwt")
            return render_template_string(
                "<h1>Authentication Error</h1><p>No valid token received. Please check your Clerk configuration.</p>"
            ), 400
        
        # Store the token in session (it should be a valid JWT)
        session['clerk_db_jwt'] = token
        session.modified = True
        return redirect('/dashboard')
    
    except Exception as e:
        logging.error(f"Error validating state parameter: {e}")
        return redirect('/auth/login')
