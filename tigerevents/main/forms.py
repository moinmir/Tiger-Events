from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from tigerevents.models import User

class SearchForm(FlaskForm):

    searchq = StringField("Search...")
    submit = SubmitField("Search")