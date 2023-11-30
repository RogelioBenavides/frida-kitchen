from flask_app import app, mysql
from flask import redirect, request, render_template, session

@app.route('/identity')
def identity():
    if not session.get('loggedin', False):
        return redirect('login')
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from identity")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC identity")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("DESC identity")
    attribute_types = [attribute_type[1] for attribute_type in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('identity.html', results = results, columns = columns, indices = indices, attribute_types = attribute_types)

@app.route('/identity/add', methods=['POST'])
def add_identity():
    if not session.get('loggedin', False):
        return redirect('login')
    
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO identity (name, last_name, username, password, is_admin)
        VALUES (%(name)s, %(last_name)s, %(username)s, %(password)s, %(is_admin)s)
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/identity')

@app.route('/identity/edit/<string:id>', methods=['POST'])
def edit_identity(id):
    if not session.get('loggedin', False):
        return redirect('login')
    
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT created_at FROM identity WHERE id = %s', (id,))
    created_at = cursor.fetchone()
    cursor.close()

    form_data['id'] = id
    form_data['created_at'] = created_at

    cursor = mysql.connection.cursor()
    query = """
        UPDATE identity SET
        name = %(name)s,
        last_name = %(last_name)s,
        username = %(username)s,
        password = %(password)s,
        is_admin = %(is_admin)s,
        created_at = %(created_at)s
        WHERE id = %(id)s
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/identity')

@app.route('/identity/delete', methods=['GET'])
def delete_identity():
    if not session.get('loggedin', False):
        return redirect('login')
    
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM identity WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/identity')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)