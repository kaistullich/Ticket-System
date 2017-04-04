import bcrypt
from flask import Flask, redirect, render_template, request, session, url_for

from ticket_system import app
from ticket_system.models import MessageForm, TicketDB, Admin, db


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
