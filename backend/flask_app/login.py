from flask_app import app, mysql, jwt
from flask import Flask, request, render_template, session, redirect
from flask_jwt_extended import create_access_token

@app.route("/login")
def login():
    return render_template('login.html')
