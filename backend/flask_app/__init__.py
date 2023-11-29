import os
from dotenv import load_dotenv
from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS

# App Creation
app = Flask(__name__)

# Set .env variabels into the os
load_dotenv()

# Loadiong the os variables as app variables
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

# Connection to the database
mysql = MySQL(app)

# Setup the Flask_JWT-Extended extension
app.secret_key = '485k5'

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

from flask_app import company
from flask_app import identity_company
from flask_app import identity
from flask_app import ingredients
from flask_app import long_stop
from flask_app import meal_ingredients
from flask_app import meals
from flask_app import order_meals
from flask_app import orders
from flask_app import payments
from flask_app import route
from flask_app import sample
from flask_app import sampling
from flask_app import short_stop
from flask_app import truck
from flask_app import uploaded_file
from flask_app import users
from flask_app import login