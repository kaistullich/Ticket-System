import json

from flask import render_template
from flask_mail import Message
from twilio.rest import Client

from src import app
from src.models import mail
from .decorators import async_

with open('src/config.json') as f:
    config_f = json.load(f)

account_sid = config_f['account_sid']
auth_token = config_f['auth_token']
client = Client(account_sid, auth_token)


# Decorator is utilized for Asynchronous tasks
@async_
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, html_body):
    """

    :param subject: the subject in the email    
    :param sender: the email sender
    :param recipients: `list` of email addresses
    :param html_body: the body for HTML, alternative :param: text_body
    :return: sends the task to the new Thread
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    send_async_email(app, msg)


def email_notification(cust_name, cust_email, tix):
    """

    :param cust_name: customer name comes from form submission
    :param cust_email: customer email comes from form submission
    :param tix: this is the ticket num, randomly generated
    """
    send_email("fitBody: Support Ticket #{tix}!".format(tix=tix),
               config_f['MAIL_USERNAME'],
               [cust_email],
               render_template("ticket_email.html",
                               c_name=cust_name, tix=tix))


def twilio_sms(cust_to, cust_name, tix_num):
    """

    :param cust_to: phone number, comes from form submission
    :param cust_name: customer name comes from form submission
    :param tix_num: this is the ticket num, randomly generated
    :return: sends the SMS
    """

    message = ("Dear {name}, your ticket #{t_num} was successfully received by fitBody! \n\n\n\
    *** DO NOT RESPOND, THIS IS AN AUTOMATED MESSAGE ***".format(name=cust_name, t_num=tix_num))

    client.messages.create(
        to=cust_to,
        from_=config_f['from_'],
        body=message
    )


def ticket_reminder_call(dept_number):
    """

    :param dept_number: the number being pulled from the DB to contact employee
    :return: initiate the call
    """
    call = client.api.account.calls.create(to=dept_number,
                                           from_=config_f['from_'],
                                           # TODO: change URL to new HTTPS ngrok url WITH /reminder
                                           url="https://27d3f05a.ngrok.io/reminder",
                                           )
    print(call.sid)


def ticket_creation_call(dept_number):
    """

    :param dept_number: the number being pulled from the DB to contact employee
    :return: initiate the call
    """
    call = client.api.account.calls.create(to=dept_number,
                                           from_=config_f['from_'],
                                           # TODO: change URL to new HTTPS ngrok url WITH /ticket_creation
                                           url="https://27d3f05a.ngrok.io/ticket_creation",
                                           )
    print(call.sid)
