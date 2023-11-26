import os
from dotenv import load_dotenv
from flask import Flask
from flask_mysqldb import MySQL

# App Creation
app = Flask(__name__)

# Set .env variabels into the os
load_dotenv()

# Loadiong the os variables as app variables
app.config['MYSQL_USER'] = os.environ.get('USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('PASSWORD')
app.config['MYSQL_HOST'] = os.environ.get('HOST')
app.config['MYSQL_DB'] = os.environ.get('DB')

# Connection to the database
mysql = MySQL(app)

# Secret Key for session purposes
app.secret_key = '485k2'

from flask_app import *

"""
# App
from .backend import app
from . import backend

# Routes
from . import ingredients
from . import meals
from . import users
from . import company
from . import payments
from . import orders
from . import identity
from . import uploaded_file
from . import identity_company
from . import sample
from . import route
from . import sampling
from . import truck
from . import short_stop
from . import long_stop
from . import meal_ingredients
from . import order_meals
"""