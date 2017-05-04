import json
import time

import bcrypt
from flask import flash, redirect, render_template, request, url_for, session
from twilio.base.exceptions import TwilioRestException
from twilio.twiml.voice_response import VoiceResponse

from src.notifications import email_notification, twilio_sms, ticket_creation_call
from src.forms import *
from src.models import Tickets, EmployeeLogin, Customers, db, app

# JSON config file
with open('src/config_values.json') as f:
    config_f = json.load(f)


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
    # Create object from `TicketForm()`
    form = TicketForm()
    # If form is fully validated and the request is of type 'POST'
    if form.validate_on_submit() and request.method == 'POST':
        # All customer entered data from the form fields
        # `First Name` field
        cust_f_name = form.f_name.data
        # `Lat Name` field
        cust_l_name = form.l_name.data
        # Make `cust_email` global to use for `/ticket_creation` route
        global cust_email
        # `Email` field
        cust_email = form.email.data
        # `Phone Number` field
        cust_phone = form.phone_number.data
        formatted_cust_phone = int(''.join(x for x in cust_phone if x.isdigit() or x == '+'))
        print(formatted_cust_phone)
        print(formatted_cust_phone)
        print(formatted_cust_phone)
        print(formatted_cust_phone)
        # `Issue` field
        tix_dept = form.ticket_type.data
        # `Business Impact` field
        tix_severity = form.severity.data
        # `Message` field
        tix_msg = form.message.data
        # Always inset new tickets with "Open" status
        tix_status = "Open"
        # Current local date
        tix_recv_date = time.strftime('%D')
        # Current local time
        tix_recv_time = time.strftime('%H%M')

        # Query Customer DB to check if customer already exists
        exist_cust = Customers.query.filter_by(cust_email=cust_email).first()

        # If customer does NOT exist
        if exist_cust is None:
            new_cust = Customers(cust_f_name=cust_f_name,
                                 cust_l_name=cust_l_name,
                                 cust_email=cust_email,
                                 cust_phone=6507876895
                                 )
            db.session.add(new_cust)
            # Submit new customer to `customers` table
            db.session.commit()
            # Get new customer ID
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
            # Submit new ticket into `tickets` table with new customer
            db.session.commit()

            # Query Tickets table to retrieve the ticketID for customer
            tickets = Tickets.query.filter_by(custID=new_cust_ID).first()
            tix_num = tickets.ticketID

            # Send off both Email / SMS notifications
            # TODO: Uncomment email_notification() when presenting
            # email_notification(cust_f_name, cust_email, tix_num)
            try:
                # TODO: Uncomment twilio_sms() for presentation
                # twilio_sms(formatted_cust_phone, cust_f_name, tix_num)
                pass
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
            # Submit new ticket with existing customer into `tickets` table
            db.session.commit()

            # Query Tickets table to retrieve the ticketID for customer
            tickets = Tickets.query.filter_by(custID=exist_cust_ID).order_by('custID').all()
            # Loop through all tickets
            ticketIDs = [t.ticketID for t in tickets]
            # Assign last ticketID to `tix_num`
            tix_num = ticketIDs[-1]

            # Send off both Email / SMS notifications
            # TODO: Uncomment email_notification() when presenting
            # email_notification(cust_f_name, cust_email, tix_num)
            try:
                # TODO: Uncomment twilio_sms() for presentation
                # twilio_sms(formatted_cust_phone, cust_f_name, tix_num)
                pass
            except TwilioRestException:
                flash('The phone number provided was unable to be reached', 'warning')

        # If the `tix_severity` was selected as P1, call agent.
        if tix_severity == '1':
            ticket_creation_call(config_f['dept_num'])
        # When form is successfully submitted flash success message
        flash('Your ticket was successfully submitted!', 'success')
        # Redirect to `/home` route when ticket is submitted
        return redirect(url_for('home'))

    # Render `login.html` template and pass `form` object along
    return render_template('home.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This route is used to log into the Flask-Admin views.
    The username and password are checked from the `login` table
    to make sure of a positive match.
    
    :return: Upon successful login, re-route to Flask-Admin view
    """

    # Create object for `LoginForm()`
    form = LoginForm()
    # If form is fully validated and the request is of type 'POST'
    if form.validate_on_submit() and request.method == 'POST':
        # `Username` field
        username = form.username.data
        # `Password` field
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
            # If password does not match flash message
            else:
                flash('That username or password does not match, try again.', 'danger')
                # Redirect to `/login` if in this block
                return redirect(url_for('login'))
        # If username does not match flash message.
        else:
            flash('That username or password does not match, try again.', 'danger')
            # Redirect to `/login` if in this block
            return redirect(url_for('login'))
    # Render `login.html` template and pass `form` object along
    return render_template('login.html', form=form)


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
        # Flash success message for logout
        flash('You have been successfully logged out!', 'success')
        # Redirect to `/home`
        return redirect(url_for('home'))
    # If `admin` NOT in the session
    else:
        # Flash the message below
        flash('You need to first sign in to logout', 'warning')
        # Redirect to `/home`
        return redirect(url_for('home'))


@app.route("/reminder", methods=['GET', 'POST'])
def ticket_reminder_route():
    """
    This route is only accessed when the `api_check.py` process
    is run. It will check the tickets for 4 conditions:
    
        1. If Ticket Severity == 1
        2. If Ticket Status == "Open"
        3. If Ticket Received Date == Today's Date
            3a. If Ticket Received Time - Time Now is >= 60
            3b. Then append the TicketID to a list
        4. Else If Ticket Received Date NOT = Today's Date
            4a. Then append the TicketID to a list
            
    :return: the response telling user the number of open tickets
    """

    # Create today's date
    date_now = time.strftime('%D')
    # Create current local time
    time_now = int(time.strftime('%H%M'))
    # Query `tickets` table for all tickets
    open_p1_tix = Tickets.query.all()
    # List that will append all matching requirement tickets
    open_p1_list = []
    # Loop through the tickets and check for the given requirements
    for t in open_p1_tix:
        if t.tix_severity == 1:
            if t.tix_status == 'Open':
                if date_now == t.tix_recv_date:
                    if time_now - t.tix_recv_time >= 60:
                        open_p1_list.append(t.ticketID)
                elif date_now != t.tix_recv_date:
                    open_p1_list.append(t.ticketID)

    # If there is only 1 matching P1 ticket
    if len(open_p1_list) == 1:
        # Create VoiceResponse object from Twilio
        resp = VoiceResponse()
        # Command given to TwiML XML
        resp.say('There is 1 open Priority 1 tickets. Please check your queue.'.format(loop=2, voice='man'))
        # Send response to route
        return str(resp)
    # If there are more than 1 matching P1 tickets
    else:
        open_p1_list = len(open_p1_list)
        # Create VoiceResponse object from Twilio
        resp = VoiceResponse()
        # Command given to TwiML XML
        resp.say('There are {num_tix} open Priority 1 tickets. Please check your queue.'.format(num_tix=open_p1_list,
                                                                                                loop=2,
                                                                                                voice='man'))
        # Send response to route
        return str(resp)


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
    tickets = Tickets.query.filter_by(cust_email=cust_email).all()
    # Loop through all tickets by given `cust_email`
    all_tickets = [t.ticketID for t in tickets]
    # Assign last P1 ticket to `last_p1_ticket`
    last_p1_ticket = all_tickets[-1]
    # Create VoiceResponse object from Twilio
    resp = VoiceResponse()
    # Command given to TwiML XML
    resp.say('A new priority 1 ticket with ID {tix_ID} has been created'.format(tix_ID=last_p1_ticket),
             loop=2,
             voice='man')
    # Send response to route
    return str(resp)
