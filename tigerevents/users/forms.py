from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from tigerevents.models import User

class RegistrationForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )

    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists.")


class LoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")

    submit = SubmitField("Login")


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("No account with that email. You must register first.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Update Password")
