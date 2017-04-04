import json
import os

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, Email, Length

from ticket_system import app

with open('ticket_system/config.json') as f:
    config_f = json.load(f)

app.secret_key = os.urandom(24)
Bootstrap(app)

app.config['DATABASE_FILE'] = config_f['DATABASE_FILE']
app.config['SQLALCHEMY_DATABASE_URI'] = config_f['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_ECHO'] = config_f['SQLALCHEMY_ECHO']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config_f['SQLALCHEMY_TRACK_MODIFICATIONS']
app.config['MAIL_SERVER'] = config_f['MAIL_SERVER']
app.config['MAIL_PORT'] = config_f['MAIL_PORT']
app.config['MAIL_USERNAME'] = config_f['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = config_f['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = config_f['MAIL_USE_TLS']
app.config['MAIL_USE_SSL'] = config_f['MAIL_USE_SSL']
db = SQLAlchemy(app)
mail = Mail(app)
admin = Admin(app, template_mode='bootstrap3')


class MessageForm(FlaskForm):
    name = StringField('Name:', [InputRequired()])
    email = StringField('Email:', [InputRequired(), Email('Invalid Email!')])
    phone_number = StringField('Phone Number:', [InputRequired(),
                                                 Length(min=10,
                                                        max=10,
                                                        message='Phone number must be 10 digits!')
                                                 ])
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
