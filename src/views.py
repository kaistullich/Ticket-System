import bcrypt
import json
import time

from flask import flash, redirect, render_template, request, url_for

from src.all_notifications import email_notification, twilio_sms, ticket_creation_call
from src.models import TicketForm, LoginForm, TicketTable, AgentLoginTable, CustomerTable, db, app

from twilio.twiml.voice_response import VoiceResponse

with open('src/config.json') as f:
    config_f = json.load(f)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = TicketForm()

    if form.validate_on_submit() and request.method == 'POST':
        # Block will be executed if ticketID did NOT match random
        cust_name = form.name.data
        global cust_email
        cust_email = form.email.data
        cust_phone = form.phone_number.data
        tix_dept = form.ticket_type.data
        tix_severity = form.severity.data
        tix_msg = form.message.data
        tix_status = "Open"
        tix_recv_date = time.strftime('%D')
        tix_recv_time = time.strftime('%H%M')

        # Query Customer DB to check if customer already exists
        exist_cust = CustomerTable.query.filter_by(cust_email=cust_email).first()

        # If customer does NOT exist
        if exist_cust is None:
            new_cust = CustomerTable(cust_name=cust_name, cust_email=cust_email, cust_phone=cust_phone)
            db.session.add(new_cust)
            db.session.commit()

        # Insert new completed ticket into TicketDB
        new_ticket = TicketTable(cust_name=cust_name, cust_email=cust_email, cust_phone=cust_phone,
                              tix_dept=tix_dept, tix_severity=tix_severity, tix_msg=tix_msg,
                              tix_status=tix_status, tix_recv_date=tix_recv_date, tix_recv_time=tix_recv_time)
        db.session.add(new_ticket)
        db.session.commit()

        # Query needed to notify ticket # by SMS
        ticket = TicketTable.query.filter_by(cust_email=cust_email).first()

        # Send off both Email / SMS notifications
        email_notification(cust_name, cust_email, ticket.ticketID)
        twilio_sms(cust_phone, cust_name, ticket.ticketID)

        # Send call to agent if new ticket submit is of severity type 1
        if tix_severity == '1':
            ticket_creation_call(config_f['dept_num'])

        flash('Your tickets was successfully submitted!', 'success')
        return redirect(url_for('home'))

    return render_template('home.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        password = form.password.data
        agent = AgentLoginTable.query.filter_by(username=username).first()

        if agent:
            psw_hash = bcrypt.checkpw(password.encode('utf-8'), agent.password.encode('utf-8'))
            if psw_hash:
                return redirect(url_for('admin.index'))
            else:
                flash(u'That username or password does not match, try again', 'warning')
                return redirect(url_for('login'))
        else:
            flash(u'That username or password does not match, try again', 'warning')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route("/reminder", methods=['GET', 'POST'])
def ticket_reminder_route():
    # TODO: Put name of dept and ticket number into voice
    resp = VoiceResponse()
    resp.say('There are {num_open_tix} open Priority 1 tickets. Please check your queue.'.format(num_open_tix='still'),
             loop=2,
             voice='man')

    return str(resp)


@app.route('/ticket_creation', methods=['GET', 'POST'])
def ticket_creation():
    # TODO: Put `tix_ID` with NEW ticket submission

    ticket = TicketTable.query.filter_by(cust_email=cust_email).first()
    resp = VoiceResponse()
    resp.say('A new priority 1 ticket with ID {tix_ID} has been created'.format(tix_ID=ticket.ticketID),
             loop=2,
             voice='man')

    return str(resp)
