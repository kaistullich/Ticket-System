import json

from flask import render_template
from flask_mail import Message
from twilio.rest import Client

from src import app
from src.config import mail
from .decorators import async_

with open('src/config_values.json') as f:
    config_f = json.load(f)

# Twilio Account SID
account_sid = config_f['account_sid']
# Twilio Authentication Token
auth_token = config_f['auth_token']
# Create object for `Client()` class and pass in the access rights
client = Client(account_sid, auth_token)


# Decorator is utilized for Asynchronous tasks (found in `decorators.py`)
@async_
def send_async_email(msg, app):
    """
    This function take email from `send_email()` and send it
    asynchronously, using threading. The `@async_` comes
    from `decorators.py`.

    :param app: Flask app
    :param msg: The HTML email (`ticket_email.html`)

    :return: send the email
    """
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, html_body):
    """
    This functions actually sends the email

    :param subject: the subject in the email
    :param sender: the email sender
    :param recipients: `list` of email addresses
    :param html_body: the body for HTML, alternative
    :return: sends the task to the new Thread
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    send_async_email(msg, app)


def email_notification(cust_name, cust_email, tix):
    """
    Prepping all the information needed to put the
    email together. It will then pass all the information
    to the `send_email()`

    :param cust_name: customer name comes from form submission
    :param cust_email: customer email comes from form submission
    :param tix: this is the ticket num, randomly generated
    """
    send_email("[Support Ticket #{tix}]".format(tix=tix),
               config_f['MAIL_USERNAME'],
               [cust_email],
               render_template("ticket_email.html",
                               c_name=cust_name, tix=tix))


@async_
def twilio_sms(cust_to, cust_name, tix_num):
    """
    Sending the SMS regarding customer new ticket
    creation. It will mention their name and the
    ticket ID for their reference.

    :param cust_to: phone number, comes from form submission
    :param cust_name: customer name comes from form submission
    :param tix_num: this is the ticket num, randomly generated
    :return: sends the SMS
    """
    with app.app_context():
        message = ("Dear {name}, your ticket #{t_num} was successfully received by Customer Support! \n\n\n\
        *** DO NOT RESPOND, THIS IS AN AUTOMATED MESSAGE ***".format(name=cust_name, t_num=tix_num))

        client.messages.create(
            to=cust_to,
            from_=config_f['from_'],
            body=message
        )


@async_
def ticket_reminder_call(dept_number):
    """
    Initiates the call for any tickets meeting the
    4 requirements set out in the `/reminder` route
    in views.py.

    :param dept_number: the number coming from `config.json`

    :return: initiate the reminder call
    """
    with app.app_context():
        call = client.api.account.calls.create(to=dept_number,
                                               from_=config_f['from_'],
                                               url=config_f['reminder'],
                                               )
        print(call.sid)


@async_
def ticket_creation_call(dept_number):
    """
    Initiates the call for any new ticket submission
    where the ticket severity == 1. Take a look at the
    `/ticket_creation` route in views.py.

    :param dept_number: the number coming from `config.json`

    :return: initiate the ticket creation call
    """
    with app.app_context():
        call = client.api.account.calls.create(to=dept_number,
                                               from_=config_f['from_'],
                                               url=config_f['ticket_creation'],
                                               )
        print(call.sid)
