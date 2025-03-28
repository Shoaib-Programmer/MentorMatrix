import os
import logging
from urllib.parse import urlencode
from flask import Blueprint, redirect, url_for, session, request, render_template, flash
from itsdangerous import URLSafeTimedSerializer

# Import your password functions and user model helpers
from app.password import hash_password, verify_password
from app.models import (
    get_user_by_email,
    get_user_by_username,
    create_standard_user,
    update_user_confirmation_status,
    update_user_password,
)
from app.forms import (
    LoginForm,
    RegisterForm,
    PasswordResetRequestForm,
    PasswordResetForm,
)

# Set up blueprint with URL prefix /auth
auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

# Initialize the serializer using the app's secret key from your config
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
serializer = URLSafeTimedSerializer(SECRET_KEY)


def generate_confirmation_token(email):
    """Generates a confirmation token for the given email."""
    return serializer.dumps(email, salt=SECRET_KEY)


def confirm_token(token, expiration=3600):
    """Validates a confirmation token and returns the email if valid."""
    try:
        email = serializer.loads(token, salt=SECRET_KEY, max_age=expiration)
    except Exception as e:
        logging.error(f"Token validation failed: {e}")
        return False
    return email


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Hash the password (now returns a single hashed string)
        hashed_password = hash_password(password)

        # Check if email is already registered
        if get_user_by_email(email):
            flash("Email is already registered!", "danger")
            return redirect(url_for("auth.register"))

        # Create a new user (with confirmed set to False)
        # Pass an empty string for salt since Argon2 embeds it in the hash.
        create_standard_user(username, email, hashed_password, confirmed=False, salt="")

        # Generate a confirmation token and build the confirmation URL
        token = generate_confirmation_token(email)
        confirm_url = url_for("auth.confirm_email", token=token, _external=True)
        html = render_template("email/confirm.html", confirm_url=confirm_url)

        # Send the confirmation email using Flask-Mail (configured in app.py)
        from app.app import mail
        from flask_mail import Message

        msg = Message("Please confirm your email", recipients=[email])
        msg.html = html
        mail.send(msg)

        flash(
            "Registration successful! A confirmation email has been sent. Please confirm your email to complete registration.",
            "success",
        )
        return redirect(url_for("dashboard.index"))
    return render_template("auth/register.html", form=form)


@auth_blueprint.route("/confirm/<token>")
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        flash("The confirmation link is invalid or has expired.", "danger")
        return redirect(url_for("dashboard.index"))
    user = get_user_by_email(email)
    if not user:
        flash("Account not found.", "danger")
        return redirect(url_for("dashboard.index"))
    if user[0]["confirmed"]:
        flash("Account already confirmed. Please log in.", "info")
    else:
        update_user_confirmation_status(email, True)
        flash("You have confirmed your account. Thanks!", "success")
    return redirect(url_for("auth.login"))


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if "user_id" in session:
        flash("You are already logged in.", "info")
        return redirect(url_for("dashboard.index"))
    if form.validate_on_submit():
        username_or_email = form.username_or_email.data
        password = form.password.data

        # Try to find user by email first, then by username
        user = get_user_by_email(username_or_email)
        if not user:
            user = get_user_by_username(username_or_email)
            if not user:
                flash("Invalid username/email or password!", "danger")
                return redirect(url_for("auth.login"))

        # Prevent OAuth-only users from logging in via password
        if user[0]["password"] in (None, "oauth"):
            flash("Please log in using your OAuth provider.", "warning")
            return redirect(url_for("auth.login"))

        # Verify password (salt not needed separately with Argon2)
        if not verify_password(password, user[0]["password"]):
            flash("Invalid username/email or password!", "danger")
            return redirect(url_for("auth.login"))

        # Save user session data
        session["user_id"] = user[0]["id"]
        session["username"] = user[0]["username"]
        flash(f"Welcome back, {user[0]['username']}!", "success")
        return redirect(url_for("dashboard.index"))
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/reset_password", methods=["GET", "POST"])
def reset_password_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        user = get_user_by_email(email)
        if user:
            token = generate_confirmation_token(email)
            reset_url = url_for("auth.reset_password", token=token, _external=True)
            html = render_template("email/reset_password.html", reset_url=reset_url)
            from app.app import mail
            from flask_mail import Message

            msg = Message("Password Reset Request", recipients=[email])
            msg.html = html
            mail.send(msg)
            flash(f"A password reset email has been sent to {email}.", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("Email not found.", "danger")
            return redirect(url_for("auth.reset_password_request"))
    return render_template("auth/reset_password_request.html", form=form)


@auth_blueprint.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = confirm_token(token)
    if not email:
        flash("The password reset link is invalid or has expired.", "danger")
        return redirect(url_for("dashboard.dashboard"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        new_password = form.password.data
        hashed_password = hash_password(new_password)
        update_user_password(email, hashed_password, salt="")
        flash("Your password has been updated!", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password_form.html", form=form)


@auth_blueprint.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("dashboard.index"))


@auth_blueprint.route("/resend_confirmation", methods=["GET", "POST"])
def resend_confirmation():
    from app.forms import ResendConfirmationForm  # Import the new form

    form = ResendConfirmationForm()
    if form.validate_on_submit():
        email = form.email.data
        user = get_user_by_email(email)
        if not user:
            flash("No account found with that email.", "danger")
            return redirect(url_for("auth.resend_confirmation"))
        if user[0]["confirmed"]:
            flash("Your account is already confirmed. Please log in.", "info")
            return redirect(url_for("auth.login"))

        # Generate a new confirmation token and build the URL
        token = generate_confirmation_token(email)
        confirm_url = url_for("auth.confirm_email", token=token, _external=True)
        html = render_template("email/confirm.html", confirm_url=confirm_url)

        # Send the confirmation email using Flask-Mail
        from app.app import mail
        from flask_mail import Message

        msg = Message("Please confirm your email", recipients=[email])
        msg.html = html
        mail.send(msg)

        flash("A new confirmation email has been sent.", "success")
        return redirect(url_for("index"))
    return render_template("auth/resend_confirmation.html", form=form)
