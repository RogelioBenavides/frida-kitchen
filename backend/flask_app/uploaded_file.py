from flask_app import app, mysql
from flask import redirect, request, render_template

@app.route('/uploaded_file')
def uploaded_file():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from uploaded_file")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC uploaded_file")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("DESC uploaded_file")
    attribute_types = [attribute_type[1] for attribute_type in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('uploaded_file.html', results = results, columns = columns, indices = indices, attribute_types = attribute_types)

@app.route('/uploaded_file/add', methods=['POST'])
def add_uploaded_file():
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO uploaded_file (filename, step, company_id)
        VALUES (%(filename)s, %(step)s, %(company_id)s)
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/uploaded_file')

@app.route('/uploaded_file/edit/<string:id>', methods=['POST'])
def edit_uploaded_file(id):
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT created_at FROM uploaded_file WHERE id = %s', (id,))
    created_at = cursor.fetchone()
    cursor.close()

    form_data['id'] = id
    form_data['created_at'] = created_at

    cursor = mysql.connection.cursor()
    query = """
        UPDATE uploaded_file SET
        filename = %(filename)s,
        step = %(step)s,
        company_id = %(company_id)s,
        created_at = %(created_at)s
        WHERE id = %(id)s
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/uploaded_file')

@app.route('/uploaded_file/delete', methods=['GET'])
def delete_uploaded_file():
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM uploaded_file WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/uploaded_file')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)