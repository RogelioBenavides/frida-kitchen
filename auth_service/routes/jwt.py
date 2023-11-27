from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from .backend import app, mysql
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    print(email, password)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from users WHERE email = %s AND user_password = %s", (email, password) )
    results = cursor.fetchall()
    print(results)
    if len(results) == 0:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)