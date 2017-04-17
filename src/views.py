import bcrypt
import json
import time

from flask import flash, redirect, render_template, request, url_for

from src.all_notifications import email_notification, twilio_sms, ticket_creation_call
from src.models import TicketForm, LoginForm, Tickets, AgentLogin, Customers, db, app

from twilio.twiml.voice_response import VoiceResponse

with open('src/config.json') as f:
    config_f = json.load(f)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    """
        - This is the main ticket submission form handled on two 
          routes (`/` & `/home`), the form can be accessed from
          either route.
    
        - On submit of the form all the form data is accessed and 
          stored immediately inside of the `tickets` table. Further,
          a new customer is created in the `customers` table. But before
          a new customer is created the table will be queried to 
          check whether or not the customer already exists in the table.
          
            - If customer already exists, the data entry will not occur.
    
        - After entry into both (or one) table, the customer will be 
          contacted via SMS and Email, utilizing Twilio's API.
    
        - If the customer submitted a P1 ticket, regardless of the 
          department, the agent of that department will receive a call
          letting them know that a new P1 ticket has been created
          along with the `ticketID`. 
            ** See /reminder route
            
    :return: - new ticket creation 
             - new customer (if not exists) 
             - send SMS/email to customer 
             - send call to agent if P1 ticket submitted
    """

    form = TicketForm()

    if form.validate_on_submit() and request.method == 'POST':
        # Block will be executed if ticketID did NOT match random
        cust_f_name = form.f_name.data
        cust_l_name = form.l_name.data
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
        exist_cust = Customers.query.filter_by(cust_email=cust_email).first()

        # If customer does NOT exist
        if exist_cust is None:
            new_cust = Customers(cust_f_name=cust_f_name,
                                 cust_l_name=cust_l_name,
                                 cust_email=cust_email,
                                 cust_phone=cust_phone
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
            twilio_sms(cust_phone, cust_f_name, tix_num)

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
            twilio_sms(cust_phone, cust_f_name, tix_num)


        if tix_severity == '1':
            ticket_creation_call(config_f['dept_num'])

        flash('Your tickets was successfully submitted!', 'success')
        return redirect(url_for('home'))

    return render_template('home.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This route is used to log into the Flask-Admin views.
    The username and password are checked from the `login` table
    to make sure of a positive match.
    
    :return: Upon successful login, re-route to Flask-Admin view
    """
    form = LoginForm()

    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        password = form.password.data
        agent = AgentLogin.query.filter_by(username=username).first()

        if agent:
            psw_hash = bcrypt.checkpw(password.encode('utf-8'), agent.password.encode('utf-8'))
            if psw_hash:
                return redirect(url_for('admin.index'))
            else:
                flash(u'That username or password does not match, try again', 'danger')
                return redirect(url_for('login'))
        else:
            flash(u'That username or password does not match, try again', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


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

    date_now = time.strftime('%D')
    time_now = int(time.strftime('%H%M'))

    open_p1_tix = Tickets.query.all()

    open_p1_list = []
    for t in open_p1_tix:
        if t.tix_severity == 1:
            if t.tix_status == 'Open':
                if date_now == t.tix_recv_date:
                    if time_now - t.tix_recv_time >= 60:
                        open_p1_list.append(t.ticketID)
                elif date_now != t.tix_recv_date:
                    open_p1_list.append(t.ticketID)

    if len(open_p1_list) == 1:
        resp = VoiceResponse()
        resp.say('There is 1 open Priority 1 tickets. Please check your queue.'.format(loop=2, voice='man'))
        return str(resp)
    else:
        open_p1_list = len(open_p1_list)
        resp = VoiceResponse()
        resp.say('There are {num_tix} open Priority 1 tickets. Please check your queue.'.format(num_tix=open_p1_list,
                                                                                                loop=2,
                                                                                                voice='man'))
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

    resp = VoiceResponse()
    resp.say('A new priority 1 ticket with ID {tix_ID} has been created'.format(tix_ID=last_p1_ticket),
             loop=2,
             voice='man')

    return str(resp)
