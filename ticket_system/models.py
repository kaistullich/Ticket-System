import os
import json

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField
from wtforms import fields, widgets
from wtforms.validators import InputRequired, Email, Length, EqualTo

from ticket_system import app

