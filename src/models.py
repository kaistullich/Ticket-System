import flask_restless
import json
import os

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField
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
class TicketForm(FlaskForm):
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
    severity = SelectField('Business Impact:', [InputRequired()],
                           choices=[('3', 'P3 - General'),
                                    ('2', 'P2 - Degraded'),
                                    ('1', 'P1 - Critical Outage')
                                    ])
    message = TextAreaField('Message:', [InputRequired()])


class LoginForm(FlaskForm):
    """
    Agent Login Form to access the Database
    """
    username = StringField('Username:', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])


# All Database Models below:
class TicketDB(db.Model):
    __tablename__ = 'tickets'

    ticketID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True, unique=True)
    cust_name = db.Column(db.String(50), nullable=False)
    cust_email = db.Column(db.String(50), nullable=False)
    cust_phone = db.Column(db.Integer, nullable=False)
    tix_dept = db.Column(db.String(30), nullable=False)
    tix_severity = db.Column(db.Integer, nullable=False)
    tix_msg = db.Column(db.String(500), nullable=False)
    tix_status = db.Column(db.String(10), nullable=False)
    tix_recv_date = db.Column(db.String(20), nullable=False)
    tix_recv_time = db.Column(db.Integer, nullable=False)


class DepartmentDB(db.Model):
    __tablename__ = 'department'

    deptID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    dept_name = db.Column(db.String(40), nullable=False)
    dept_empl = db.Column(db.String(40), nullable=False)
    dept_empl_phone = db.Column(db.Integer, nullable=False)


class CustomerDB(db.Model):
    __tablename__ = 'customers'

    custID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_name = db.Column(db.String(50), nullable=False)
    cust_email = db.Column(db.String(60), nullable=False)
    cust_phone = db.Column(db.Integer, nullable=False)


class AgentLoginDB(db.Model):
    __tablename__ = 'login'

    username = db.Column(db.String(4), primary_key=True)
    password = db.Column(db.String(60))


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
admin.add_view(TicketAdminView(TicketDB, db.session, menu_icon_type='glyph', menu_icon_value='glyphicon-home'))
admin.add_view(DepartmentAdminView(DepartmentDB, db.session))
admin.add_view(CustomersAdminView(CustomerDB, db.session))

# API Manager
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(TicketDB,
                   methods=['GET', 'POST']
                   )
