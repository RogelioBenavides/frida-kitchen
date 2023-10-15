from flask import render_template
from app import app
from flask_socketio import SocketIO

sio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')