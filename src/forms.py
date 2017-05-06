from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SelectField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length

from src.models import dept_choice


class TicketForm(FlaskForm):
    """
    Ticket form found on URL route `/` & `/home`. Includes
    certain validators for form submission
    """

    # `First Name` HTML input field
    f_name = StringField('First Name:',
                         [InputRequired()],
                         render_kw={'placeholder': 'First Name'}
                         )

    # `Last Name` HTML input field
    l_name = StringField('Last Name:',
                         [InputRequired()],
                         render_kw={'placeholder': 'Last Name'}
                         )

    # `Email` HTML input field
    email = StringField('Email:',
                        [InputRequired(),
                         Email('Invalid Email!')],
                        render_kw={'placeholder': 'ex. support@support.org'}
                        )

    # `Phone Number` HTML input field
    phone_number = StringField('Phone Number:',
                               [InputRequired(),
                                # Min length of 10 digit
                                Length(min=14,
                                       # Max length of 10 digit
                                       max=14,
                                       # Message if not correct length
                                       message='Phone number must be 10 digits!')
                                ],
                               render_kw={'placeholder': 'ex. (555) 555-5555'}
                               )

    # `Issue Type` HTML input field
    ticket_type = SelectField('Select an issue:',
                              [InputRequired()],
                              choices=dept_choice()
                              )

    # `Severity` HTML input field
    severity = SelectField('Issue Severity:',
                           [InputRequired()],
                           choices=[('P3', 'P3 - General'),
                                    ('P2', 'P2 - Degraded'),
                                    ('P1', 'P1 - Critical Outage')
                                    ]
                           )

    # `Message` HTML input field
    message = TextAreaField('Message:',
                            [InputRequired()],
                            render_kw={'placeholder': 'Please describe the issue...'}
                            )

    # `reCAPTCHA` HTML input field
    recaptcha = RecaptchaField()

    # `Submit` HTML button
    submit = SubmitField()


class LoginForm(FlaskForm):
    """
    Agent Login Form to access Flask-Admin views
    """

    # `Username` HTML input field
    username = StringField('Username:',
                           [InputRequired()],
                           render_kw={'placeholder': 'Username'}
                           )

    # `Password` HTML input field
    password = PasswordField('Password',
                             [InputRequired()],
                             render_kw={'placeholder': 'Password'}
                             )


class ChatForm(FlaskForm):
    username = StringField('Name:',
                           [InputRequired()],
                            render_kw={'placeholder': 'Name'}
                           )

    message = TextAreaField('Message:',
                            [InputRequired()],
                            render_kw={'placeholder': 'Message'}
                            )
