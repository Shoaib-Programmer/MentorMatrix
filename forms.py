from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    username_or_email = StringField(
        "Username or Email", 
        validators=[DataRequired(), Length(max=50)]
    )
    password = PasswordField(
        "Password", 
        validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters long")]
    )
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField(
        "Username", 
        validators=[DataRequired(), Length(max=50)]
    )
    email = StringField(
        "Email", 
        validators=[DataRequired(), Email(message="Invalid email"), Length(max=50)]
    )
    password = PasswordField(
        "Password", 
        validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters long")]
    )
    submit = SubmitField("Register")

