from flask_wtf import FlaskForm, CSRFProtect

from wtforms import StringField, TextField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, Optional

csrf = CSRFProtect()


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(message="Name cannot be empty")])
    email = StringField('Email', validators=[DataRequired(
        message="E-mail cannot be empty"), Email("Enter a valid email(abc@example.xyz)")])
    subject = StringField('Subject', validators=[
                          DataRequired(message="Subject cannot be empty")])
    message = TextAreaField('Message', validators=[DataRequired(
        message="Message cannot be empty"), Length(min=2, max=100)])
    # submit=SubmitField('Submit')


class FormTaskCreate(FlaskForm):
    title = StringField(
            'Title',
            validators=[DataRequired(message="Field cannot be empty!")],
            render_kw={'size':31}
        )
    description = TextAreaField(
            'Description',
            validators=[
                DataRequired(),
                Length(min=3, max=150, message="Field must be between 3 and 150 characters long!")
            ],
            render_kw={'cols':35, 'rows': 5}
        )
    priority = SelectField(
        'Priority',
        choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high')]
    )
    submit = SubmitField('Submit')

class FormTaskUpdate(FlaskForm):
    title = StringField(
            'Title',
            validators=[DataRequired(message="Field cannot be empty!")],
            render_kw={'size':31}
        )
    description = TextAreaField(
            'Description',
            validators=[
                DataRequired(),
                Length(min=3, max=150, message="Field must be between 3 and 150 characters long!")
            ],
            render_kw={'cols':35, 'rows': 5}
        )
    created = DateField(
        'Created'
        # default=datetime.today()
         # format='%Y-%m-%d'
    )
    priority = SelectField(
        'Priority',
        choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high')]
    )
    is_done = BooleanField(
        'is_done'
    )
    submit = SubmitField('Submit')
