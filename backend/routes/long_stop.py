from .backend import app, mysql
from flask import redirect, request, render_template

@app.route('/long_stop')
def long_stop():
    # Obtén el número total de registros en la tabla
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) from long_stop")
    total_records = cursor.fetchone()[0]

    # Obtén el número de página actual desde la solicitud del usuario
    page = request.args.get('page', default=1, type=int)

    # Define el número de resultados por página
    per_page = 50  # Número de resultados por página

    # Calcula el número total de páginas
    total_pages = (total_records + per_page - 1) // per_page

    # Calcula el valor de offset
    offset = (page - 1) * per_page

    # Calcula el rango de páginas a mostrar (por ejemplo, 10 páginas)
    page_range = 10
    start_page = max(1, page - (page_range // 2))
    end_page = min(total_pages, start_page + page_range - 1)

    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * from long_stop LIMIT {per_page} OFFSET {offset}")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC long_stop")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("DESC long_stop")
    attribute_types = [attribute_type[1] for attribute_type in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('long_stop.html', results=results, columns=columns, indices=indices, attribute_types=attribute_types, page=page, total_pages=total_pages, start_page=start_page, end_page=end_page)

@app.route('/long_stop/add', methods=['POST'])
def add_long_stop():
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO long_stop (latitude, longitude, start_time, end_time,, duration,  aux1, aux2, aux3)
        VALUES (%(latitude)s, %(longitude)s, %(start_time)s, %(end_time)s, %(duration)s, %(aux1)s, %(aux2)s, %(aux3)s)
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/long_stop')

@app.route('/long_stop/edit/<string:id>', methods=['POST'])
def edit_long_stop(id):
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT created_at FROM long_stop WHERE id = %s', (id,))
    created_at = cursor.fetchone()
    cursor.close()

    form_data['id'] = id
    form_data['created_at'] = created_at

    cursor = mysql.connection.cursor()
    query = """
        UPDATE long_stop SET
        latitude = %(latitude)s,
        longitude = %(longitude)s,
        start_time = %(start_time)s,
        end_time = %(end_time)s,
        duration = %(duration)s,
        created_at = %(created_at)s,
        aux1 = %(aux1)s,
        aux2 = %(aux2)s,
        aux3 = %(aux3)s
        WHERE id = %(id)s
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/long_stop')

@app.route('/long_stop/delete', methods=['GET'])
def delete_long_stop():
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM long_stop WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/long_stop')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)