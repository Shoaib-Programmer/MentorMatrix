from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Enter a username"},
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=255)],
        render_kw={"placeholder": "Enter your email"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)],
        render_kw={"placeholder": "Enter a password"},
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
        render_kw={"placeholder": "Confirm your password"},
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username_or_email = StringField(
        "Username or Email",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your username or email"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your password"},
    )
    submit = SubmitField("Login")


class PasswordResetRequestForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Enter your email"},
    )
    submit = SubmitField("Request Password Reset")


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        "New Password",
        validators=[DataRequired(), Length(min=6)],
        render_kw={"placeholder": "Enter a new password"},
    )
    confirm = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
        render_kw={"placeholder": "Confirm your new password"},
    )
    submit = SubmitField("Reset Password")



class ResendConfirmationForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Resend Confirmation")
