from flask import Flask

app = Flask(__name__)
from ticket_system.views import app
