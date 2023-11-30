from flask_app import app, mysql
from flask import redirect, request, render_template, session

@app.route('/orders')
def orders():
    if not session.get('loggedin', False):
        return redirect('login')
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from orders")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC orders")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("DESC orders")
    attribute_types = [attribute_type[1] for attribute_type in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('orders.html', results = results, columns = columns, indices = indices, attribute_types = attribute_types)

@app.route('/orders/add', methods=['POST'])
def add_order():
    if not session.get('loggedin', False):
        return redirect('login')
    
    form_data = request.form.to_dict(flat=True)

    print(form_data)

    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO orders (id_route, id_user)
        VALUES (%(id_route)s, %(id_user)s)
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/orders')

@app.route('/orders/edit/<string:id>', methods=['POST'])
def edit_order(id):
    if not session.get('loggedin', False):
        return redirect('login')
    
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT created_at FROM orders WHERE id = %s', (id,))
    created_at = cursor.fetchone()
    cursor.close()

    form_data['id'] = id
    form_data['created_at'] = created_at

    cursor = mysql.connection.cursor()
    query = """
        UPDATE orders SET
        id_route = %(id_route)s,
        id_user = %(id_user)s,
        created_at = %(created_at)s
        WHERE id = %(id)s
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/orders')

@app.route('/orders/delete', methods=['GET'])
def delete_order():
    if not session.get('loggedin', False):
        return redirect('login')
    
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM orders WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/orders')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)