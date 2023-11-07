from .backend import app, mysql
from flask import redirect, request, render_template

@app.route('/identity_company')
def identity_company():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from identity_company")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC identity_company")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("DESC identity_company")
    attribute_types = [attribute_type[1] for attribute_type in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('identity_company.html', results = results, columns = columns, indices = indices, attribute_types = attribute_types)

@app.route('/identity_company/add', methods=['POST'])
def add_identity_company():
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO identity_company (identity_id, company_id)
        VALUES (%(identity_id)s, %(company_id)s)
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/identity_company')

@app.route('/identity_company/edit/<string:id>', methods=['POST'])
def edit_identity_company(id):
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT created_at FROM identity_company WHERE id = %s', (id,))
    created_at = cursor.fetchone()
    cursor.close()

    form_data['id'] = id
    form_data['created_at'] = created_at

    cursor = mysql.connection.cursor()
    query = """
        UPDATE identity_company SET
        identity_id = %(identity_id)s,
        company_id = %(company_id)s,
        created_at = %(created_at)s
        WHERE id = %(id)s
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/identity_company')

@app.route('/identity_company/delete', methods=['GET'])
def delete_identity_company():
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM identity_company WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/identity_company')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)