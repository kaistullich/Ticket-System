import json

from flask import render_template
from flask_mail import Message

from ticket_system import app
from ticket_system.models import mail
from .decorators import async_

from twilio.rest import Client

with open('ticket_system/config.json') as f:
    config_f = json.load(f)


@async_
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    send_async_email(app, msg)


def email_notification(cust_name, cust_email, tix):
    send_email("fitBody: Support Ticket #{tix}!".format(tix=tix),
               config_f['MAIL_USERNAME'],
               [cust_email],
               render_template("ticket_email.html",
                               c_name=cust_name, tix=tix))


def twilio_sms(cust_to, cust_name, tix_num):
    # Twilio Auth
    account_sid = config_f['account_sid']
    auth_token = config_f['auth_token']

    client = Client(account_sid, auth_token)

    client.messages.create(
        to=cust_to,
        from_=config_f['from_'],
        body="Dear {name}, your ticket #{t_num} was successfully received by fitBody! \
                *** DO NOT RESPOND, THIS IS AN AUTOMATED MESSAGE ***".format(name=cust_name, t_num=tix_num)
    )
