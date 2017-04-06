import json
from random import randrange

from flask import flash, redirect, render_template, request, url_for

from src.all_notifications import email_notification, twilio_sms
from src.models import MessageForm, TicketDB, db, app

from twilio.twiml.voice_response import VoiceResponse


with open('src/config.json') as f:
    config_f = json.load(f)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    rand_num = randrange(100, 1000000)
    form = MessageForm()
    if form.validate_on_submit() and request.method == 'POST':
        name = form.name.data
        email = form.email.data
        number = form.phone_number.data
        message = form.message.data

        new_ticket = TicketDB(name=name, ticket_num=rand_num, email=email, message=message)
        db.session.add(new_ticket)
        db.session.commit()

        ticket = TicketDB.query.filter_by(ticket_num=rand_num).first()

        email_notification(name, email, rand_num)
        twilio_sms(number, name, ticket.ticket_num)

        flash('Your tickets was successfully submitted!', 'success')
        return redirect(url_for('home'))

    return render_template('home.html', form=form)


@app.route("/words", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming requests."""
    resp = VoiceResponse()
    resp.say("Hello Olaf Stullich, how are you today? It is a nice day outside, it is currently 3:52PM in Morgan Hill, California. Good bye!")

    return str(resp)
