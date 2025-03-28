from argon2 import PasswordHasher, exceptions

# Create a PasswordHasher instance with default parameters.
ph = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Hashes the provided password using Argon2.

    Args:
        password (str): The plaintext password.

    Returns:
        str: The hashed password (includes salt and parameters).
    """
    return ph.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """
    Verifies a plaintext password against the provided Argon2 hash.

    Args:
        password (str): The plaintext password.
        hashed (str): The previously hashed password.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    try:
        return ph.verify(hashed, password)
    except exceptions.VerifyMismatchError:
        return False
