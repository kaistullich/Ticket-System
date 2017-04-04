import os
import json

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Email

from ticket_system import app

with open('ticket_system/config.json') as f:
    config_f = json.load(f)

app.secret_key = os.urandom(24)
Bootstrap(app)

app.config['DATABASE_FILE'] = config_f['DATABASE_FILE']
app.config['SQLALCHEMY_DATABASE_URI'] = config_f['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_ECHO'] = config_f['SQLALCHEMY_ECHO']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config_f['SQLALCHEMY_TRACK_MODIFICATIONS']
db = SQLAlchemy(app)
admin = Admin(app, template_mode='bootstrap3')


class MessageForm(FlaskForm):
    name = StringField('Name:', [InputRequired()])
    email = StringField('Email:', [InputRequired(), Email('Invalid Email!')])
    message = TextAreaField('Message:', [InputRequired()])


class TicketDB(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    message = db.Column(db.String(500))


class TicketAdminView(ModelView):
    create_template = 'create.html'
    edit_template = 'edit.html'

admin.add_view(TicketAdminView(TicketDB, db.session))