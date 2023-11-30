from flask_app import app, mysql
from flask import redirect, request, render_template, jsonify, session
from http import HTTPStatus

@app.route('/users')
def users():
    if not session.get('loggedin', False):
        return redirect('login')
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from users")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC users")
    columns = [column[0] for column in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('users.html', results = results, columns = columns, indices = indices)

@app.route('/users/add', methods=['POST'])
def add_user():
    if not session.get('loggedin', False):
        return redirect('login')
    
    user_name = request.form['user_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['user_password']
    role = request.form['user_role']

    if user_name and last_name and email and password and role:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (user_name, last_name, email, user_password, user_role) VALUES (%s, %s, %s, %s, %s)", (user_name, last_name, email, password, role))
        mysql.connection.commit()
        cursor.close()
    return redirect('/users')

@app.route('/users/frontAdd', methods=['POST'])
def add_user_front():
    if not session.get('loggedin', False):
        return redirect('login')
    
    user_name = request.json.get('user_name', None)
    last_name = request.json.get('last_name', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from users WHERE email = %s AND user_password = %s", (email, password) )
    results = cursor.fetchall()
    if len(results) != 0:
        return jsonify({"msg": "Email already registered"}), HTTPStatus.BAD_REQUEST
    
    if user_name and last_name and email and password:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (user_name, last_name, email, user_password, user_role) VALUES (%s, %s, %s, %s, 'customer')", (user_name, last_name, email, password))
        mysql.connection.commit()
        cursor.close()
    return jsonify({"msg": "User added"}), HTTPStatus.OK

@app.route('/users/edit/<string:id>', methods=['POST'])
def edit_user(id):
    if not session.get('loggedin', False):
        return redirect('login')
    
    user_name = request.form['user_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['user_password']
    role = request.form['user_role']

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT created_at FROM users WHERE id = %s', (id,))
    created_at = cursor.fetchone()
    cursor.close()

    if user_name and last_name and email and password and role:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET user_name = %s, last_name = %s, email = %s, user_password = %s, user_role = %s, created_at = %s WHERE id = %s", (user_name, last_name, email, password, role, created_at, id))
        mysql.connection.commit()
        cursor.close()
    return redirect('/users')

@app.route('/users/delete', methods=['GET'])
def delete_user():
    if not session.get('loggedin', False):
        return redirect('login')
    
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM users WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/users')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)