from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from datetime import datetime

app = Flask(__name__)

load_dotenv()

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

mysql = MySQL(app)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/coords', methods=["GET"])
def get_coords():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT latitude, longitude FROM sample")
        results = cursor.fetchall()
        cursor.close()

        coords = [{'lat': row[0], 'lng': row[1]} for row in results]

        return jsonify({'coords': coords})

    except Exception as e:
        return jsonify({'error': str(e)}), 500