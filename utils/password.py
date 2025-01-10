from argon2 import PasswordHasher # type: ignore
from argon2.exceptions import VerifyMismatchError # type: ignore

ph = PasswordHasher()

def hash_password(plain_password):
    import os
    salt = os.urandom(16).hex()  # Generate a random salt
    salted_password = plain_password + salt  # Append the salt to the password
    hashed_password = ph.hash(salted_password)  # Hash the salted password
    return hashed_password, salt

def verify_password(plain_password, hashed_password, salt):
    try:
        salted_password = plain_password + salt  # Append the salt to the provided password
        return ph.verify(hashed_password, salted_password)  # Verify using salted password
    except VerifyMismatchError:
        return False
