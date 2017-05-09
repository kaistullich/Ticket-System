import json
import os
import sys

from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from src import app

# JSON config file
with open('src/config_values.json') as f:
    config_f = json.load(f)


def db_uri(system):
    """
    Check system type for database URI setup
    
    :param system: `sys.platform()` will be passed in
    :return: system type
    """
    # Mac
    if system == 'darwin':
        uri = 'sqlite:////' + os.getcwd() + '/ticket_system.sqlite'
    # Windows
    elif system == 'win32':
        uri = r'sqlite:///' + os.getcwd() + '\ticket_system.sqlite'
    # Linux
    elif system == 'linux':
        uri = 'sqlite:////' + os.getcwd() + '/ticket_system.sqlite'
    # Linux2
    elif system == 'linux2':
        uri = 'sqlite:////' + os.getcwd() + '/ticket_system.sqlite'
    # If system could not be determined
    else:
        raise FileNotFoundError('SQLite File was not able to be found')
    # Return system type
    return uri


# All configuration needed for Flask
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri(sys.platform)
app.config['DATABASE_FILE'] = config_f['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = config_f['SQLALCHEMY_ECHO']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config_f['SQLALCHEMY_TRACK_MODIFICATIONS']
app.config['MAIL_SERVER'] = config_f['MAIL_SERVER']
app.config['MAIL_PORT'] = config_f['MAIL_PORT']
app.config['MAIL_USERNAME'] = config_f['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = config_f['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = config_f['MAIL_USE_TLS']
app.config['MAIL_USE_SSL'] = config_f['MAIL_USE_SSL']
app.config['RECAPTCHA_PUBLIC_KEY'] = config_f['cap_pub']
app.config['RECAPTCHA_PRIVATE_KEY'] = config_f['cap_sec']

Bootstrap(app)
db = SQLAlchemy(app)
mail = Mail(app)
admin = Admin(app, name='Tickets', template_mode='bootstrap3')
socketio = SocketIO(app)
