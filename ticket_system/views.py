import bcrypt
from flask import Flask, redirect, render_template, request, session, url_for

from ticket_system import app
from ticket_system.models import *
