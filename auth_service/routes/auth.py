from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager
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

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get('SECRET_KEY')
jwt = JWTManager(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from users WHERE email = %s AND user_password = %s", (email, password) )
    results = cursor.fetchall()
    if len(results) == 0:
        return jsonify({"msg": "Bad username or password"}), 401
        
    access_token = create_access_token(identity=email)
    return jsonify({"access_token": access_token, "user": results[0][0], "role": results[0][5]})