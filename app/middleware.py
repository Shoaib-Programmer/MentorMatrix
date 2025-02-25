import requests
from functools import wraps
from flask import request, jsonify, g, redirect, session # type: ignore
import jwt  # noqa: E402

def get_clerk_public_keys():
    # Adjust the URL according to Clerk's documentation
    response = requests.get("https://api.clerk.dev/public-keys")
    if response.status_code != 200:
        raise Exception("Failed to fetch Clerk public keys")
    # Assume the response is a JSON object mapping key IDs (kid) to public keys.
    return response.json()


def verify_clerk_token(token):
    # Get the unverified header to determine which key was used to sign the token
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.PyJWTError as e:
        print("Error reading token header:", e)
        return None

    kid = unverified_header.get("kid")
    if not kid:
        print("Token header missing 'kid'")
        return None

    # Fetch the public keys from Clerk
    public_keys = get_clerk_public_keys()
    key = public_keys.get(kid)
    if not key:
        print("Appropriate public key not found for kid:", kid)
        return None

    try:
        # Decode and verify the token using the RS256 algorithm
        payload = jwt.decode(token, key, algorithms=["RS256"])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token expired")
    except jwt.InvalidTokenError as e:
        print("Invalid token:", e)
    return None


def requires_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # First, try to get the token from the Authorization header
        auth_header = request.headers.get("Authorization")
        token = None
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            # Fallback: try to get the token from the session
            token = session.get("token")
        
        if not token:
            # If no token is found, redirect to login
            return redirect('/auth/login')

        payload = verify_clerk_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401

        # Store the token payload in Flask's global context if needed
        g.clerk_payload = payload
        return f(*args, **kwargs)
    return decorated_function

