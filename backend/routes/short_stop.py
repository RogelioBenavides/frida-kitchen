from .backend import app, mysql
from flask import redirect, request, render_template

@app.route('/short_stop')
def short_stop():
    # Obtén el número total de registros en la tabla
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) from short_stop")
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
    cursor.execute(f"SELECT * from short_stop LIMIT {per_page} OFFSET {offset}")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC short_stop")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("DESC short_stop")
    attribute_types = [attribute_type[1] for attribute_type in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('short_stop.html', results=results, columns=columns, indices=indices, attribute_types=attribute_types, page=page, total_pages=total_pages, start_page=start_page, end_page=end_page)

@app.route('/short_stop/add', methods=['POST'])
def add_short_stop():
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO short_stop (route_id, latitude, longitude, start_time, end_time, distance_to_next_stop, duration,  aux1, aux2, aux3)
        VALUES (%(route_id)s, %(latitude)s, %(longitude)s, %(start_time)s, %(end_time)s, %(distance_to_next_stop)s, %(duration)s, %(aux1)s, %(aux2)s, %(aux3)s)
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/short_stop')

@app.route('/short_stop/edit/<string:id>', methods=['POST'])
def edit_short_stop(id):
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT created_at FROM short_stop WHERE id = %s', (id,))
    created_at = cursor.fetchone()
    cursor.close()

    form_data['id'] = id
    form_data['created_at'] = created_at

    cursor = mysql.connection.cursor()
    query = """
        UPDATE short_stop SET
        route_id = %(route_id)s,
        latitude = %(latitude)s,
        longitude = %(longitude)s,
        start_time = %(start_time)s,
        end_time = %(end_time)s,
        distance_to_next_stop = %(distance_to_next_stop)s,
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
    return redirect('/short_stop')

@app.route('/short_stop/delete', methods=['GET'])
def delete_short_stop():
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM short_stop WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/short_stop')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)