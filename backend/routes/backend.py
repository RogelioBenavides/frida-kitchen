from flask import Flask, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from flask_cors import CORS
import os

app = Flask(__name__, template_folder='templates')

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

load_dotenv()

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

mysql = MySQL(app)

@app.route('/')
def index():
    return 'puerto 5000'
