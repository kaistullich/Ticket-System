import json
import os
import sys

from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_mail import Mail
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
    elif system == 'linux2':
        uri = 'sqlite:////' + os.getcwd() + '/ticket_system.sqlite'
    # If system could not be determined
    else:
        raise FileNotFoundError('SQLite File was not able to be found')
    # Return system type
    return uri


# All configuration needed for Flask
app.secret_key = os.urandom(24)
# Path to SQLite DB
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri(sys.platform)
# Name of SQLite file
app.config['DATABASE_FILE'] = config_f['DATABASE_FILE']
# Echo SQLAlchemy into console
app.config['SQLALCHEMY_ECHO'] = config_f['SQLALCHEMY_ECHO']
# Suppress warning in console form SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config_f['SQLALCHEMY_TRACK_MODIFICATIONS']
# Mail server (i.e. Gmail)
app.config['MAIL_SERVER'] = config_f['MAIL_SERVER']
# Mail port
app.config['MAIL_PORT'] = config_f['MAIL_PORT']
# Username for mail server account
app.config['MAIL_USERNAME'] = config_f['MAIL_USERNAME']
# Password for mail server account
app.config['MAIL_PASSWORD'] = config_f['MAIL_PASSWORD']
# If to use TLS
app.config['MAIL_USE_TLS'] = config_f['MAIL_USE_TLS']
# If to use SSL
app.config['MAIL_USE_SSL'] = config_f['MAIL_USE_SSL']
# Google reCAPTCHA public key
app.config['RECAPTCHA_PUBLIC_KEY'] = config_f['cap_pub']
# Google reCAPTCHA private key
app.config['RECAPTCHA_PRIVATE_KEY'] = config_f['cap_sec']

# Create multiple objects for different libraries
Bootstrap(app)
# Instantiate SQLAlchemy DB
db = SQLAlchemy(app)
# Instantiate Flask-Mail
mail = Mail(app)
# Instantiate Flask-Admin Model
admin = Admin(app, template_mode='bootstrap3')
