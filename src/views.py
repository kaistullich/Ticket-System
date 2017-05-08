import json
import time

import bcrypt
from flask import flash, redirect, render_template, request, url_for, session, Markup
from flask_socketio import emit, join_room, leave_room
from twilio.base.exceptions import TwilioRestException
from twilio.twiml.voice_response import VoiceResponse

from src.config import socketio
from src.forms import *
from src.models import Tickets, EmployeeLogin, Customers, db, app
from src.notifications import email_notification, twilio_sms, ticket_creation_call

# JSON config file
with open('src/config_values.json') as f:
    config_f = json.load(f)


#-----------------------------------------
# ~~~~~~~~~~~~~~~~~ HOME ~~~~~~~~~~~~~~~~~
#-----------------------------------------


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    """
        - This is the main ticket submission form handled on two 
          routes (`/` & `/home`), the form can be accessed from
          either route.
    
        - On submit of the form all the form data is accessed and 
          stored  inside of the `tickets` table. Further, a new customer 
          is created in the `customers` table. But before
          a new customer is created the table will be queried to 
          check whether or not the customer already exists in the table.
          To check if a a customer already exists we will use their email
          address as a unique identifier, given that usually an email address
          can only be assigned to a single person.
          
            - If customer already exists, no new customer entry will occur.
    
        - After entry into both (or one) table, the customer will be 
          contacted via SMS and Email, utilizing Twilio's API for SMS.
    
        - If the customer submitted a P1 ticket, regardless of the 
          department, the agent of that department will receive a call
          letting them know that a new P1 ticket has been created
          along with the `ticketID`. 
            ** See `/ticket_creation` route
            
    :return: - new ticket creation 
             - new customer (if not exists) 
             - send SMS/email to customer 
             - send call to agent if P1 ticket submitted
    """

    form = TicketForm()

    if form.validate_on_submit() and request.method == 'POST':
        # All customer entered data from the form fields

        cust_f_name = form.f_name.data
        cust_l_name = form.l_name.data
        cust_email = form.email.data
        cust_phone = form.phone_number.data
        formatted_cust_phone = int(''.join(x for x in cust_phone if x.isdigit() or x == '+'))
        tix_dept = form.ticket_type.data
        tix_severity = form.severity.data
        tix_msg = form.message.data
        tix_status = "Open"
        tix_recv_date = time.strftime('%D')
        tix_recv_time = time.strftime('%H%M')

        # Query Customer DB to check if customer already exists
        exist_cust = Customers.query.filter_by(cust_email=cust_email).first()

        # If customer does NOT exist
        if exist_cust is None:
            new_cust = Customers(cust_f_name=cust_f_name,
                                 cust_l_name=cust_l_name,
                                 cust_email=cust_email,
                                 cust_phone=formatted_cust_phone
                                 )
            db.session.add(new_cust)
            db.session.commit()

            new_cust_ID = new_cust.custID

            # Insert ticket into Tickets for new customer
            new_ticket = Tickets(custID=new_cust_ID,
                                 tix_dept=tix_dept,
                                 tix_severity=tix_severity,
                                 tix_msg=tix_msg,
                                 tix_status=tix_status,
                                 tix_recv_date=tix_recv_date,
                                 tix_recv_time=tix_recv_time
                                 )
            db.session.add(new_ticket)
            db.session.commit()

            # Query Tickets table to retrieve the ticketID for customer
            tickets = Tickets.query.filter_by(custID=new_cust_ID).first()
            tix_num = tickets.ticketID

            # Send off both Email / SMS notifications
            email_notification(cust_f_name, cust_email, tix_num)
            try:
                twilio_sms(formatted_cust_phone, cust_f_name, tix_num)
            except TwilioRestException:
                flash('The phone number provided was unable to be reached', 'warning')

        # If customer already exists
        else:
            # Assigns existing custID to `exist_cust_ID`
            exist_cust_ID = exist_cust.custID

            # Insert ticket in to Tickets for existing customer
            new_ticket = Tickets(custID=exist_cust_ID,
                                 tix_dept=tix_dept,
                                 tix_severity=tix_severity,
                                 tix_msg=tix_msg,
                                 tix_status=tix_status,
                                 tix_recv_date=tix_recv_date,
                                 tix_recv_time=tix_recv_time
                                 )
            db.session.add(new_ticket)
            db.session.commit()

            # Query Tickets table to retrieve the ticketID for customer
            tickets = Tickets.query.filter_by(custID=exist_cust_ID).order_by('custID').all()
            # Loop through all tickets
            ticketIDs = [t.ticketID for t in tickets]
            # Assign last ticketID to `tix_num`
            tix_num = ticketIDs[-1]

            # Send off both Email / SMS notifications
            email_notification(cust_f_name, cust_email, tix_num)
            try:
                twilio_sms(formatted_cust_phone, cust_f_name, tix_num)
            except TwilioRestException:
                flash('The phone number provided was unable to be reached', 'warning')

        # If the `tix_severity` was selected as P1, call agent.
        if tix_severity == 'P1':
            ticket_creation_call(config_f['dept_num'])

        flash('Your ticket was successfully submitted!', 'success')
        return redirect(url_for('home'))

    return render_template('home.html', form=form)


#-----------------------------------------
# ~~~~~~~~~~~TICKET STATUS ~~~~~~~~~~~~~~~
#-----------------------------------------

@app.route('/ticket_status', methods=['GET', 'POST'])
def ticket_status():

    form = TicketStatusForm()

    if form.validate_on_submit() and request.method == 'POST':
        ticket_num = form.tix_num.data
        ticket = Tickets.query.filter_by(ticketID=ticket_num).first()
        if ticket is not None:
            customer = Customers.query.filter_by(custID=ticket.custID).first()
            return render_template('ticket_status.html', ticket=ticket, customer=customer)
        else:
            flash('We do not have that ticket # on file, please double check!', 'warning')

    return render_template('ticket_status_form.html', form=form)


#-----------------------------------------
# ~~~~~~~~~~~~~~~~~ Login ~~~~~~~~~~~~~~~~
#-----------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This route is used to log into the Flask-Admin views.
    The username and password are checked from the `login` table
    to make sure of a positive match.
    
    :return: Upon successful login, re-route to Flask-Admin view
    """
    if 'admin' not in session:

        form = LoginForm()

        if form.validate_on_submit() and request.method == 'POST':

            username = form.username.data
            password = form.password.data
            # Query `Login` table to pull `username` (there is only 1 entry in the `username` column)
            agent = EmployeeLogin.query.filter_by(username=username).first()

            # If username matches
            if agent:
                # Check if password entered matches hash in `password` columns in `Login` table
                psw_hash = bcrypt.checkpw(password.encode('utf-8'), agent.password.encode('utf-8'))
                # If password matches hash
                if psw_hash:
                    # Start session for 'admin'
                    session['admin'] = username
                    return redirect(url_for('admin.index'))
                # If password does not
                else:
                    flash('That username or password does not match, try again.', 'danger')
                    return redirect(url_for('login'))
            # If username does not
            else:
                flash('That username or password does not match, try again.', 'danger')
                return redirect(url_for('login'))

    else:
        return redirect(url_for('admin.index'))

    return render_template('login.html', form=form)


#-----------------------------------------
# ~~~~~~~~~~~~~~~~~ Logout ~~~~~~~~~~~~~~~
#-----------------------------------------

@app.route('/logout')
def logout():
    """
    Logout `admin` from the session to re-protect the `/admin` route
    
    If `admin` is not in the session we will redirect to the home route,
    but flash a different message
    
    :return: redirect to home & drop session if allowed
    """

    # If session object matches what is in session
    if 'admin' in session:
        # Drop session for `admin`
        session.pop('admin', None)
        flash('You have been successfully logged out!', 'success')
        return redirect(url_for('home'))

    # If `admin` NOT in the session
    else:
        flash('You need to first sign in to logout', 'warning')
        return redirect(url_for('home'))


#-----------------------------------------
# ~~~~~~~~~~~~~~~~~ REMINDER ~~~~~~~~~~~~~
#-----------------------------------------

@app.route("/reminder", methods=['GET', 'POST'])
def ticket_reminder_route():
    """
    This route is only accessed when the `api_check.py` process
    is run. It will check the tickets for 4 conditions:
    
        1. If Ticket Severity == P1
        2. If Ticket Status == "Open"
        3. If Ticket Received Date == Today's Date
            3a. If Ticket Received Time - Time Now is >= 60
            3b. Then append the TicketID to a list
        4. Else If Ticket Received Date NOT = Today's Date
            4a. Then append the TicketID to a list
            
    :return: the response telling user the number of open tickets
    """

    date_now = time.strftime('%D')
    time_now = int(time.strftime('%H%M'))

    # Query `tickets` table for all tickets
    open_p1_tix = Tickets.query.all()

    open_p1_list = []
    # Loop through the tickets and check for the given requirements
    for t in open_p1_tix:
        if t.tix_severity == 'P1':
            if t.tix_status == 'Open':
                if date_now == t.tix_recv_date:
                    if time_now - t.tix_recv_time >= 60:
                        open_p1_list.append(t.ticketID)
                elif date_now != t.tix_recv_date:
                    open_p1_list.append(t.ticketID)

    # If there is only 1 matching P1 ticket
    if len(open_p1_list) == 1:
        resp = VoiceResponse()
        resp.say('There is 1 open Priority 1 tickets. Please check your queue.'.format(loop=2, voice='man'))
        return str(resp)

    # If there are more than 1 matching P1 tickets
    else:
        open_p1_list = len(open_p1_list)
        resp = VoiceResponse()
        resp.say('There are {num_tix} open Priority 1 tickets. Please check your queue.'.format(num_tix=open_p1_list,
                                                                                                loop=2,
                                                                                                voice='man'))
        return str(resp)


#-----------------------------------------
# ~~~~~~~~~~~~~~TIX CREATION ~~~~~~~~~~~~~
#-----------------------------------------

@app.route('/ticket_creation', methods=['GET', 'POST'])
def ticket_creation():
    """
    This route is only accessed when a NEW Priority 1 ticket 
    is submitted to the Database. The `tickets` table is then
    queried to check for the `ticketID` through a customers
    email address.
    
    It will check if the customer has submitted a ticket before.
    If a customer HAS submitted a ticket before then it will 
    retrieve the LAST tickets submitted, which is the most
    current one.
    
    :return: response telling agent the P1 `ticketID`
    """

    # Query Tickets table to pull `ticketID` by `cust_email`
    tickets = Tickets.query.filter_by(tix_severity='P1').all()
    # Loop through all tickets by given `cust_email`
    all_tickets = [t.ticketID for t in tickets]
    # Assign last P1 ticket to `last_p1_ticket`
    last_p1_ticket = all_tickets[-1]

    resp = VoiceResponse()
    resp.say('A new priority 1 ticket with ID {tix_ID} has been created'.format(tix_ID=last_p1_ticket),
             loop=2,
             voice='man')
    return str(resp)


#-----------------------------------------
# ~~~~~~~~~~~~~~ CHAT LOGIN ~~~~~~~~~~~~~~
#-----------------------------------------

@app.route('/chat_login', methods=['GET', 'POST'])
def chat_login():
    """"Login form to enter a room."""
    form = ChatLoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('chat_login.html', form=form)


#-----------------------------------------
# ~~~~~~~~~~~~~~~~~ CHAT ~~~~~~~~~~~~~~~~~
#-----------------------------------------

@app.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
            the session."""
    form = ChatForm()
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('chat_login'))
    return render_template('chat.html', name=name, room=room, form=form)


#-----------------------------------------
# ~~~~~~~~~~~~~ JOINED ~~~~~~~~~~~~~~~~~~
#-----------------------------------------
@socketio.on('joined', namespace='/chat')
def joined(message):
    """
    Sent when a certain user enters a room
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    try:
        emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)
    except TypeError:
        pass


#-----------------------------------------
# ~~~~~~~~~~~~~~~~~ TEXT ~~~~~~~~~~~~~~~~~
#-----------------------------------------

@socketio.on('text', namespace='/chat')
def text(message):
    """
    Sent when a certain user sends a message
    The message is sent to all people in the room."""
    room = session.get('room')
    name = Markup('<strong style="color: green;">' + session.get('name') + '</strong>')
    emit('message', {'msg': name + ': ' + message['msg']}, room=room)


#-----------------------------------------
# ~~~~~~~~~~~~~~~~~ LEFT ~~~~~~~~~~~~~~~~~
#-----------------------------------------

@socketio.on('left', namespace='/chat')
def left(message):
    """
    Sent when a certain user exits the room
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)
