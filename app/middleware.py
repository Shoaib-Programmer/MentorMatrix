import os
import logging
import requests  # For fetching JWKS
from functools import wraps
from flask import request, g, redirect, session
from jose import jwt

# Configuration (set these as environment variables)
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")  # e.g., 'my-domain.us.auth0.com'
# AUTH0_AUDIENCE = "https://dev-nlswp33on5rnohcr.us.auth0.com/api/v2/"
ALGORITHMS = ["RS256"]
ISSUER = f"https://{AUTH0_DOMAIN}/"


def get_session_token(req):
    """
    Extract token from the Authorization header or from session.
    """
    auth_header = req.headers.get("Authorization")
    logging.debug(f"Authorization header: {auth_header}")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    token = session.get("auth0_id_token")
    logging.debug(f"Session token (auth0_id_token): {token}")
    return token


def verify_token(token):
    """
    Verify the JWT token using Auth0's JWKS.
    Returns the decoded payload if verification is successful; otherwise, returns None.
    """
    try:
        jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
        jwks = requests.get(jwks_url).json()
        unverified_header = jwt.get_unverified_header(token)
    except Exception as e:
        logging.error(f"Error fetching JWKS or decoding header: {e}")
        return None

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header.get("kid"):
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
            break

    if not rsa_key:
        logging.error("Unable to find appropriate key")
        return None

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            issuer=ISSUER,
            options={"verify_aud": False}
        )
        return payload
    except jwt.ExpiredSignatureError:
        logging.error("Token expired")
    except jwt.JWTClaimsError as e:
        logging.error(f"Invalid claims: {e}")
    except Exception as e:
        logging.error(f"Token verification error: {e}")
    return None


def verify_user(req):
    token = get_session_token(req)
    if not token:
        logging.debug("No token found in request")
        return None
    payload = verify_token(token)
    if payload:
        logging.debug(f"Verified user payload: {payload}")
    return payload


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_payload = verify_user(request)
        if not user_payload:
            # Clear session if verification fails and redirect to login.
            session.clear()
            return redirect("/auth/login")
        # Attach the token payload to Flask's global context.
        g.user = user_payload
        logging.debug(f"Authenticated user: {g.user.get('sub')}")
        return f(*args, **kwargs)

    return decorated
