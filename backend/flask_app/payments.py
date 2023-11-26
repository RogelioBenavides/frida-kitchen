from flask_app import app, mysql
from flask import redirect, request, render_template

@app.route('/payments')
def payments():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from payments")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC payments")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("DESC payments")
    attribute_types = [attribute_type[1] for attribute_type in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('payments.html', results = results, columns = columns, indices = indices, attribute_types = attribute_types)

@app.route('/payments/add', methods=['POST'])
def add_payment():
    form_data = request.form.to_dict(flat=True)

    print(form_data)

    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO payments (id_order, payment_method, payment_amount)
        VALUES (%(id_order)s, %(payment_method)s, %(payment_amount)s)
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/payments')

@app.route('/payments/edit/<string:id>', methods=['POST'])
def edit_payment(id):
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT payment_date FROM payments WHERE id = %s', (id,))
    payment_date = cursor.fetchone()
    cursor.close()

    form_data['id'] = id
    form_data['payment_date'] = payment_date

    cursor = mysql.connection.cursor()
    query = """
        UPDATE payments SET
        id_order = %(id_order)s,
        payment_method = %(payment_method)s,
        payment_amount = %(payment_amount)s,
        payment_date = %(payment_date)s
        WHERE id = %(id)s
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/payments')

@app.route('/payments/delete', methods=['GET'])
def delete_payment():
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM payments WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/payments')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)