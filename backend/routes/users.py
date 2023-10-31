from .backend import app, mysql
from flask import redirect, request, render_template

@app.route('/users')
def users():
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

@app.route('/users/edit/<string:id>', methods=['POST'])
def edit_user(id):
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
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM users WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/users')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)