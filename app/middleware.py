import os
import logging
from functools import wraps
from flask import request, g, redirect, session
import httpx
from clerk_backend_api import Clerk
from clerk_backend_api.jwks_helpers import AuthenticateRequestOptions

# Initialize a Clerk client instance once
clerk_client = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

def get_session_token(req):
    # First try to extract token from the Authorization header
    auth_header = req.headers.get('Authorization')
    logging.debug(f"Authorization header: {auth_header}")
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split(' ')[1]
    # Fall back to the token stored in session under 'clerk_db_jwt'
    token = session.get('clerk_db_jwt')
    logging.debug(f"Session token (clerk_db_jwt): {token}")
    return token

def verify_user(req):
    token = get_session_token(req)
    if not token:
        logging.debug("No token found in request")
        return None
    try:
        # Construct a dummy httpx.Request with the token in the Authorization header.
        headers = {"Authorization": f"Bearer {token}"}
        fake_request = httpx.Request("GET", "http://dummy", headers=headers)
        # Supply the required options argument. Replace with your actual authorized domain.
        options = AuthenticateRequestOptions(authorized_parties=["https://your-domain.com"])
        # Pass the dummy request object to authenticate_request.
        user_data = clerk_client.authenticate_request(fake_request, options)
        logging.debug(f"User data: {user_data}")
        return user_data
    except Exception as e:
        logging.error(f"Error verifying token: {e}")
        return None

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_data = verify_user(request)
        if not user_data:
            # Clear session if token verification fails and redirect to login.
            session.clear()
            return redirect("/auth/login")
        # Attach verified user data to Flask's global context for downstream access.
        g.user = user_data
        # logging.info(f"Authenticated user: {g.user.payload.get('sub')} from {request.remote_addr}")
        logging.debug(f"RequestState object: {g.user.__dict__}")
        return f(*args, **kwargs)
    return decorated
