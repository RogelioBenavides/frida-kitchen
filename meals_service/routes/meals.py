from flask import Flask, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

mysql = MySQL(app)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/meals/<string:id>')
def meal(id):
    print("ID: ", id)
    cursor = mysql.connection.cursor()
    print("SELECT * from meals WHERE id = %s", (id,))
    cursor.execute("SELECT * from meals WHERE id = %s", (id,))
    results = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    dict_results = [dict(zip(columns, row)) for row in results]
    jsonify(dict_results)
    return jsonify(dict_results)

@app.route('/meals/json')
def mealsJson():
    cursor = mysql.connection.cursor()

    # Execute the query
    cursor.execute("SELECT * from meals")

    # Fetch all results
    results = cursor.fetchall()

    # Get column names from the cursor description
    columns = [column[0] for column in cursor.description]

    # Convert each row into a dictionary
    dict_results = [dict(zip(columns, row)) for row in results]

    return jsonify(dict_results)

@app.route('/meals/favorites')
def mealsFavorites():
    cursor = mysql.connection.cursor()

    # Execute the query with a limit of 9 results
    cursor.execute("SELECT * FROM meals LIMIT 9")

    # Fetch all results
    results = cursor.fetchall()

    # Get column names from the cursor description
    columns = [column[0] for column in cursor.description]

    # Convert each row into a dictionary
    dict_results = [dict(zip(columns, row)) for row in results]

    return jsonify(dict_results)