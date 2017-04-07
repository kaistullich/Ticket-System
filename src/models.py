import json
import os

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email, Length

from src import app

with open('src/config.json') as f:
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


# All Forms below:
class MessageForm(FlaskForm):
    name = StringField('Name:', [InputRequired()])
    email = StringField('Email:', [InputRequired(), Email('Invalid Email!')])
    phone_number = StringField('Phone Number:', [InputRequired(),
                                                 Length(min=10,
                                                        max=10,
                                                        message='Phone number must be 10 digits!')
                                                 ])
    ticket_type = SelectField('Select an issue:', [InputRequired()], choices=[('subscription', 'Subscriptions'),
                                                                              ('maps', 'Google Maps'),
                                                                              ('profile', 'Personal Profile'),
                                                                              ('shipping', 'Shipping'),
                                                                              ('apparel', 'Apparel'),
                                                                              ('other', 'other')
                                                                              ])
    severity = SelectField('Provide the severity of the ticket:', [InputRequired()],
                                  choices=[('1', '1 - High Priority'),
                                           ('2', '2 - Medium Priority'),
                                           ('3', '3 - Low Priority')
                                           ])
    message = TextAreaField('Message:', [InputRequired()])


# All Database Models below:
class TicketDB(db.Model):
    __tablename__ = 'Ticket'

    ticketID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    ticket_group = db.Column(db.String(30), nullable=False)
    ticket_severity = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(500), nullable=False)
    ticket_status = db.Column(db.String(10), nullable=False)
    ticket_date = db.Column(db.String(20), nullable=False)
    ticket_time = db.Column(db.Integer, nullable=False)


class DepartmentDB(db.Model):
    __tablename__ = 'Department'

    deptID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    deptName = db.Column(db.String(25), nullable=False)
    agentID = db.Column(db.Integer, nullable=False)


class CustomerDB(db.Model):
    __tablename__ = 'Customers'

    custID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_name = db.Column(db.String(50), nullable=False)
    cust_email = db.Column(db.String(60), nullable=False)
    cust_phone = db.Column(db.Integer, nullable=False)


class AgentDB(db.Model):
    __tablename__ = 'Agents'

    agentID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    agent_name = db.Column(db.String(45))
    agent_phone = db.Column(db.Integer)


# All Admin Views for each table
class TicketAdminView(ModelView):
    create_template = 'create.html'
    edit_template = 'edit.html'


class DepartmentAdminView(ModelView):
    create_template = 'create.html'
    edit_template = 'edit.html'


class CustomersAdminView(ModelView):
    create_template = 'create.html'
    edit_template = 'edit.html'


class AgentsAdminView(ModelView):
    create_template = 'create.html'
    edit_template = 'edit.html'


# All Admin Views for DB's below:
admin.add_view(TicketAdminView(TicketDB, db.session))
admin.add_view(DepartmentAdminView(DepartmentDB, db.session))
admin.add_view(CustomersAdminView(CustomerDB, db.session))
admin.add_view(AgentsAdminView(AgentDB, db.session))
