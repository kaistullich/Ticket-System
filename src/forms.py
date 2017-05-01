from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SelectField, PasswordField
from wtforms.validators import InputRequired, Email, Length

from src.models import dept_choice


class TicketForm(FlaskForm):
    """
    Ticket form found on URL route `/` & `/home`. Includes
    certain validators for form submission
    """
    f_name = StringField('First Name:', [InputRequired()])
    l_name = StringField('Last Name:', [InputRequired()])
    email = StringField('Email:', [InputRequired(), Email('Invalid Email!')])
    phone_number = StringField('Phone Number:', [InputRequired(),
                                                 Length(min=10,
                                                        max=10,
                                                        message='Phone number must be 10 digits!')
                                                 ])
    ticket_type = SelectField('Select an issue:', [InputRequired()], choices=dept_choice())
    severity = SelectField('Business Impact:', [InputRequired()],
                           choices=[('3', 'P3 - General'),
                                    ('2', 'P2 - Degraded'),
                                    ('1', 'P1 - Critical Outage')
                                    ])
    message = TextAreaField('Message:', [InputRequired()])
    recaptcha = RecaptchaField()


class LoginForm(FlaskForm):
    """
    Agent Login Form to access Flask-Admin views
    """
    username = StringField('Username:', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
