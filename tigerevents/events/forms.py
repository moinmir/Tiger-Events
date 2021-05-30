from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, InputRequired, NumberRange


class EventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    location = TextAreaField("Location", validators=[DataRequired()])
    start_date = DateField("DatePicker", format='%Y-%m-%d-%h', validators=[DataRequired()])
    end_date = DateField("DatePicker", format='%Y-%m-%d-%h', validators=[DataRequired()])
    submit = SubmitField("Post")