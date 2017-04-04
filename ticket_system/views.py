import bcrypt
from flask import flash, redirect, render_template, request, url_for

from ticket_system import app
from ticket_system.models import MessageForm, TicketDB, Admin, db


@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
def home():
    form = MessageForm()
    if form.validate_on_submit() and request.method == 'POST':
        name = form.name.data
        email = form.email.data
        message = form.message.data

        new_ticket = TicketDB(name=name, email=email, message=message)
        db.session.add(new_ticket)
        db.session.commit()
        flash('Your tickets was successfully submitted!')
        return redirect(url_for('home'))

    return render_template('home.html', form=form)
