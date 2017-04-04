import bcrypt
import json
from flask import flash, redirect, render_template, request, url_for
from flask_mail import Message
from ticket_system.models import MessageForm, TicketDB, Admin, db, app, mail

with open('ticket_system/config.json') as f:
    config_f = json.load(f)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = MessageForm()
    if form.validate_on_submit() and request.method == 'POST':
        name = form.name.data
        email = form.email.data
        message = form.message.data

        new_ticket = TicketDB(name=name, email=email, message=message)
        db.session.add(new_ticket)
        db.session.commit()
        msg = Message(subject='Ticket Received!',
                      sender=config_f['MAIL_USERNAME'],
                      recipients=[email],
                      html='<p>Dear {name},</p>\
                            <p>We have received your ticket and one of our dedicated team members \
                            will work on this as soon as possible.</p>\
                            Kind Regards,</p>\
                            <p>fitBody Customer Support</p>'.format(name=name))
        mail.send(msg)
        flash('Your tickets was successfully submitted!')
        return redirect(url_for('home'))

    return render_template('home.html', form=form)
