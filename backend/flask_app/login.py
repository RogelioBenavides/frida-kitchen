from flask_app import app, mysql
from flask import Flask, request, render_template, session, redirect

@app.route('/')
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    return redirect('/login')

@app.route("/pythonlogin", methods=['GET', 'POST'])
def pythonlogin():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #Extract Credentials
        _user = request.form['username']
        _password = request.form['password']

        #Validate in MySQL
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s AND user_password = %s;', (_user, _password))
        account = cursor.fetchone()
        cursor.close()

        if not account:
            return render_template('login.html', msg='Incorrect username or password')
        
        if account[5] != 'admin':
            return render_template('login.html', msg='Your user is not an administrator')
        
        session['loggedin'] = True
        session['email'] = account[3]

        return redirect('/meals')

