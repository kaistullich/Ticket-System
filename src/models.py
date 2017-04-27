import flask_restless
from flask_admin.contrib.sqla import ModelView

from src._app_config import db, admin, app


class Tickets(db.Model):
    """
    `tickets` table creation with a relationship between
    `department` and `customers` tables:
     
    -   Create a one-to-one relationship on `tix_dept` inside of
        the `tickets` table and `deptID` inside of the `department`
        table
        
    -   Create a one-to-many relationship on `custID` in the `tickets`
        table and the `customers` table.

    """
    __tablename__ = 'tickets'

    ticketID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True, unique=True)
    custID = db.Column(db.Integer, db.ForeignKey('customers.custID'))
    tix_dept = db.Column(db.Integer, db.ForeignKey('department.deptID'))
    tix_severity = db.Column(db.String(2), nullable=False)
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


def dept_choice():
    """
    Queries the `department` table and pulls the `dept_name`
    and the `deptID`. It will then loop through the entire
    `department` table and append `deptID` & `dept_names` to
    lists.

    :return: zip of `deptID` & `dept_name`
    """
    dept = Departments.query.all()

    # Names of all departments
    dept_names = []
    # ID's for all departments
    dept_ids = []

    for d in dept:
        dept_names.append(str(d.dept_name))
        dept_ids.append(str(d.deptID))

    # zip together `dept_ids` & `dept_names`
    zipped = list(zip(dept_ids, dept_names))

    return zipped


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


class EmployeeLogin(db.Model):
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

    # `Tickets` column names
    column_labels = dict(ticketID='Ticket ID',
                         tix_severity='Ticket Severity',
                         tix_msg='Ticket Description',
                         tix_status='Ticket Status',
                         tix_recv_date='Received Date',
                         tix_recv_time='Received Time')

    # Search on following columns
    column_searchable_list = ('ticketID',
                              'tix_severity',
                              'tix_status',
                              Customers.cust_f_name,
                              Customers.cust_l_name,
                              Customers.cust_email,
                              Customers.cust_phone,
                              Departments.dept_name)

    def _message_formatter(view, context, model, name):
        # Reduce the amount of the `tix_msg` shown inside of Flask-Admin (19 characters)
        return model.tix_msg[:20]

    column_formatters = {
        'tix_msg': _message_formatter,
    }


class DepartmentAdminView(ModelView):
    """
    Creates the `department` admin view in Flask-Admin
    """
    create_template = 'create.html'
    edit_template = 'edit.html'

    # `Department` column names
    column_labels = dict(dept_name='Department',
                         dept_empl='Department Employee',
                         dept_empl_phone='Employee Phone Number'
                         )


class CustomersAdminView(ModelView):
    """
    Creates the `customer` admin view in Flask-Admin
    """
    column_display_pk = True
    create_template = 'create.html'
    edit_template = 'edit.html'

    # `Customers` column names
    column_labels = dict(custID='Customer ID',
                         cust_f_name='First Name',
                         cust_l_name='Last Name',
                         cust_email='Email',
                         cust_phone='Phone Number',
                         )


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
