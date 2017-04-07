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

    found = False
    tix_num_que = TicketDB.query.all()
    for n in tix_num_que:
        if n.ticketID == rand_num:
            found = True
            new_rand_num = randrange(10, 100000)

    if form.validate_on_submit() and request.method == 'POST':

        if not found:
            name = form.name.data
            email = form.email.data
            number = form.phone_number.data
            tix_type = form.ticket_type.data
            severity = form.severity.data
            message = form.message.data
            status = "open"

            new_ticket = TicketDB(ticketID=rand_num, name=name, email=email, ticket_group=tix_type,
                                  ticket_severity=severity, message=message, ticket_status=status)
            db.session.add(new_ticket)
            db.session.commit()

            ticket = TicketDB.query.filter_by(ticketID=rand_num).first()

            email_notification(name, email, rand_num)
            twilio_sms(number, name, ticket.ticketID)

            flash('Your tickets was successfully submitted!', 'success')
            return redirect(url_for('home'))

        else:
            name = form.name.data
            email = form.email.data
            number = form.phone_number.data
            tix_type = form.ticket_type.data
            severity = form.severity.data
            message = form.message.data
            status = "open"

            new_ticket = TicketDB(ticketID=new_rand_num, name=name, email=email, ticket_group=tix_type,
                                  ticket_severity=severity, message=message, ticket_status=status)
            db.session.add(new_ticket)
            db.session.commit()

            ticket = TicketDB.query.filter_by(ticketID=new_rand_num).first()

            email_notification(name, email, rand_num)
            twilio_sms(number, name, ticket.ticketID)

            flash('Your tickets was successfully submitted!', 'success')
            return redirect(url_for('home'))

    return render_template('home.html', form=form)


@app.route("/words", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming requests."""
    tix_severity = TicketDB.query.all()
    for tickets in tix_severity:
        pass
    resp = VoiceResponse()
    resp.say("")

    return str(resp)
