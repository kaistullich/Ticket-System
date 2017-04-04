import json

from flask import render_template
from flask_mail import Message

from ticket_system import app
from ticket_system.models import mail
from .decorators import async_


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


def notification(c_name, c_email):
    send_email("Support Ticket Received!",
               config_f['MAIL_USERNAME'],
               [c_email],
               render_template("follower_email.html",
                               c_name=c_name))
