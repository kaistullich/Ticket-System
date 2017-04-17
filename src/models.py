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

# JSON config file
with open('src/config.json') as f:
    config_f = json.load(f)

# All configuration needed for Flask
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.getcwd() + '/ticket_system.sqlite'
app.config['DATABASE_FILE'] = config_f['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = config_f['SQLALCHEMY_ECHO']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config_f['SQLALCHEMY_TRACK_MODIFICATIONS']
app.config['MAIL_SERVER'] = config_f['MAIL_SERVER']
app.config['MAIL_PORT'] = config_f['MAIL_PORT']
app.config['MAIL_USERNAME'] = config_f['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = config_f['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = config_f['MAIL_USE_TLS']
app.config['MAIL_USE_SSL'] = config_f['MAIL_USE_SSL']

# Create multiple objects for different libraries
Bootstrap(app)
db = SQLAlchemy(app)
mail = Mail(app)
admin = Admin(app, template_mode='bootstrap3')


class LoginForm(FlaskForm):
    """
    Agent Login Form to access Flask-Admin views
    """
    username = StringField('Username:', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])


class Tickets(db.Model):
    """
    `tickets` table creation with a relationship btwn `department`.
    Creating a one-to-one relationship on `tix_dept` inside of
    the `tickets` table and `deptID` inside of the `department`
    table
    """
    __tablename__ = 'tickets'

    ticketID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True, unique=True)
    custID = db.Column(db.Integer,  db.ForeignKey('customers.custID'))
    tix_dept = db.Column(db.Integer, db.ForeignKey('department.deptID'))
    tix_severity = db.Column(db.Integer, nullable=False)
    tix_msg = db.Column(db.String(500), nullable=False)
    tix_status = db.Column(db.String(10), nullable=False)
    tix_recv_date = db.Column(db.String(20), nullable=False)
    tix_recv_time = db.Column(db.Integer, nullable=False)

    # define relationship
    department = db.relationship('Departments')
    customer = db.relationship('Customers')



class Departments(db.Model):
    """
    `department` table creation
    """
    __tablename__ = 'department'

    deptID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    dept_name = db.Column(db.String(40), nullable=False)
    dept_empl = db.Column(db.String(40), nullable=False)
    dept_empl_phone = db.Column(db.Integer, nullable=False)

    def __str__(self):
        """
        method is used to display the `dept_name` instead of
        the actual object memory location

        :return: dept_name
        """
        return self.dept_name


class Customers(db.Model):
    """
    `customers` table creation
    """
    __tablename__ = 'customers'

    custID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_f_name = db.Column(db.String(30), nullable=False)
    cust_l_name = db.Column(db.String(30), nullable=False)
    cust_email = db.Column(db.String(60), nullable=False)
    cust_phone = db.Column(db.Integer, nullable=False)

    def __str__(self):
        """
        method is used to display the `cust_f_name` instead of
        the actual object memory location

        :return: cust_f_name
        """
        return self.cust_f_name


def dept_choice():
    """
    Queries the `department` table and pulls the `dept_name`
    and the `deptID`. It will then loop through the entire
    `department` table and append `deptID` & `dept_names` to
    lists.
    
    :return: zip of `deptID` & `dept_name`
    """
    dept = Departments.query.all()
    dept_names = []
    dept_ids = []
    for d in dept:
        dept_names.append(str(d.dept_name))
        dept_ids.append(str(d.deptID))

    zipped = list(zip(dept_ids, dept_names))
    return zipped


class TicketForm(FlaskForm):
    """
    Ticket form found on URL route `/` & `/home`. Includes
    certain validators for form submission
    """
    f_name = StringField('First Name:', [InputRequired()])
    l_name = StringField('Last Name:', [InputRequired()])
    email = StringField('Email:', [InputRequired(), Email('Invalid Email!')])
    phone_number = StringField('Phone Number:', [InputRequired(),
                                                 Length(min=10,
                                                        max=10,
                                                        message='Phone number must be 10 digits!')
                                                 ])
    ticket_type = SelectField('Select an issue:', [InputRequired()], choices=dept_choice())
    severity = SelectField('Business Impact:', [InputRequired()],
                           choices=[('3', 'P3 - General'),
                                    ('2', 'P2 - Degraded'),
                                    ('1', 'P1 - Critical Outage')
                                    ])
    message = TextAreaField('Message:', [InputRequired()])


class AgentLogin(db.Model):
    """
    agent `login` table creation. This table will only hold
    the username & password for logging into Flask-Admin views
    for employees
    """
    __tablename__ = 'login'

    username = db.Column(db.String(4), primary_key=True)
    password = db.Column(db.String(60))


class TicketAdminView(ModelView):
    """
    Creates the `tickets` admin view in Flask-Admin. It also 
    sets "readonly" methods on certain fields with the 
    `form_widget_args` argument
    """
    column_display_pk = True
    create_template = 'create.html'
    edit_template = 'edit.html'
    # Creates read only fields inside of `tickets` Flask-Admin view
    # TODO: Change this to create the read only fields dynamically
    form_widget_args = {
        'ticketID': {
            'readonly': True
        },
        'cust_name': {
            'readonly': True
        },
        'cust_email': {
            'readonly': True
        },
        'cust_phone': {
            'readonly': True
        },
        'tix_severity': {
            'readonly': True
        },
        'tix_msg': {
            'readonly': True
        },
        'tix_recv_date': {
            'readonly': True
        },
        'tix_recv_time': {
            'readonly': True
        }
    }


class DepartmentAdminView(ModelView):
    """
    Creates the `department` admin view in Flask-Admin
    """
    create_template = 'create.html'
    edit_template = 'edit.html'


class CustomersAdminView(ModelView):
    """
    Creates the `customer` admin view in Flask-Admin
    """
    column_display_pk = True
    create_template = 'create.html'
    edit_template = 'edit.html'


# All Flask-Admin Views
admin.add_view(TicketAdminView(Tickets, db.session, menu_icon_type='glyph', menu_icon_value='glyphicon-home'))
admin.add_view(DepartmentAdminView(Departments, db.session))
admin.add_view(CustomersAdminView(Customers, db.session))

"""
 Creates the API Manager
 
 :route: 127.0.0.1:5000/api/tickets
"""
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Tickets,
                   methods=['GET', 'POST'],
                   results_per_page=-1,
                   max_results_per_page=-1
                   )
