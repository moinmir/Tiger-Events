from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError


class EventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    location = TextAreaField("Location", validators=[DataRequired()])
    start_date = DateField("Event Start", format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField("Event End", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField("Post")

    def validate_date(self, start_date, end_date):
        if end_date <= start_date:
            raise ValidationError('Incorrect start and end times.')

