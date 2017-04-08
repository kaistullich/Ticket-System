import bcrypt
import json
import time
from random import randrange

from flask import flash, redirect, render_template, request, url_for

from src.all_notifications import email_notification, twilio_sms, ticket_call
from src.models import TicketForm, LoginForm, TicketDB, AgentLoginDB, db, app

from twilio.twiml.voice_response import VoiceResponse

with open('src/config.json') as f:
    config_f = json.load(f)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    rand_num = randrange(100, 1000000)
    form = TicketForm()

    found = False
    tix_num_que = TicketDB.query.all()
    for n in tix_num_que:
        """
        Loops through all the TicketID's and sees if there is a match 
        between the `rand_num` and a TicketID in the TicketDB. If a match 
        is found, then `Found` changes to `True` and `new_rand_num` 
        is assigned.
        """
        if n.ticketID == rand_num:
            found = True
            new_rand_num = randrange(10, 100000)

    if form.validate_on_submit() and request.method == 'POST':
        # Block will be executed if ticketID did NOT match random
        if not found:
            name = form.name.data
            email = form.email.data
            number = form.phone_number.data
            tix_type = form.ticket_type.data
            severity = form.severity.data
            message = form.message.data
            status = "Open"
            tix_date = time.strftime('%a, %d %b %Y')
            tix_time = time.strftime('%H%M')

            # Insert new completed ticket into TicketDB
            new_ticket = TicketDB(ticketID=rand_num, name=name, email=email, ticket_group=tix_type,
                                  ticket_severity=severity, message=message, ticket_status=status, ticket_date=tix_date,
                                  ticket_time=tix_time)
            db.session.add(new_ticket)
            db.session.commit()

            # Query needed to notify ticker # by SMS
            ticket = TicketDB.query.filter_by(ticketID=rand_num).first()

            # Send off both Email / SMS notifications
            email_notification(name, email, rand_num)
            twilio_sms(number, name, ticket.ticketID)

            flash('Your tickets was successfully submitted!', 'success')
            return redirect(url_for('home'))

        # Block will be executed if ticketID MATCHED random
        else:
            name = form.name.data
            email = form.email.data
            number = form.phone_number.data
            tix_type = form.ticket_type.data
            severity = form.severity.data
            message = form.message.data
            status = "Open"
            tix_date = time.strftime('%a, %d %b %Y')
            tix_time = time.strftime('%H%M')

            # Insert new completed ticket into TicketDB
            new_ticket = TicketDB(ticketID=new_rand_num, name=name, email=email, ticket_group=tix_type,
                                  ticket_severity=severity, message=message, ticket_status=status, ticket_date=tix_date,
                                  ticket_time=tix_time)
            db.session.add(new_ticket)
            db.session.commit()

            # Query needed to notify ticker # by SMS
            ticket = TicketDB.query.filter_by(ticketID=new_rand_num).first()

            # Send off both Email / SMS notifications
            email_notification(name, email, rand_num)
            twilio_sms(number, name, ticket.ticketID)

            flash('Your tickets was successfully submitted!', 'success')
            return redirect(url_for('home'))

    return render_template('home.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        password = form.password.data
        agent = AgentLoginDB.query.filter_by(username=username).first()

        if agent:
            psw_hash = bcrypt.checkpw(password.encode('utf-8'), agent.password.encode('utf-8'))
            if psw_hash:
                return redirect(url_for('admin.index'))
        else:
            flash(u'That username or password does not match, try again', 'warning')

    return render_template('login.html', form=form)


@app.route("/words", methods=['GET', 'POST'])
def ticket_voice():
    """Respond to incoming requests."""
    # TODO: Put name of dept and ticket number into voice

    resp = VoiceResponse()
    resp.say("A new Priority 1 ticket has been created and assigned to the {dept} team. Ticket number {t_num}. \
             Please log in within 1 hour to respond to the ticket.".format(dept='Database', t_num=''), loop=3)

    return str(resp)
