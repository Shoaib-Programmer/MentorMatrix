import logging
from functools import wraps
from flask import request, g, redirect, session


def verify_user(req):
    """
    For our custom authentication, simply check if 'user_id' exists in the session.
    If it does, return a basic user payload; otherwise, return None.
    """
    user_id = session.get("user_id")
    if not user_id:
        logging.debug("No user_id found in session.")
        return None
    # Build a user payload from session data (expand as needed)
    user_payload = {"id": user_id, "username": session.get("username")}
    logging.debug(f"Verified user payload: {user_payload}")
    return user_payload


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_payload = verify_user(request)
        if not user_payload:
            session.clear()
            return redirect("/auth/login")
        # Attach the user payload to Flask's global context
        g.user = user_payload
        logging.debug(f"Authenticated user: {g.user.get('username')}")
        return f(*args, **kwargs)

    return decorated
