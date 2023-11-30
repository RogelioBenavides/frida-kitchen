from flask_app import app, mysql
from flask import redirect, request, render_template, session

@app.route('/sample')
def sample():
    if not session.get('loggedin', False):
        return redirect('login')
    
    # Obtén el número total de registros en la tabla
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) from sample")
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
    cursor.execute(f"SELECT * from sample LIMIT {per_page} OFFSET {offset}")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC sample")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("DESC sample")
    attribute_types = [attribute_type[1] for attribute_type in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('sample.html', results=results, columns=columns, indices=indices, attribute_types=attribute_types, page=page, total_pages=total_pages, start_page=start_page, end_page=end_page)

@app.route('/sample/add', methods=['POST'])
def add_sample():
    if not session.get('loggedin', False):
        return redirect('login')
    
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO sample (latitude, longitude, datetime, company_id, route_id, truck_id, truck_name, duration_interval, distance, speed, status_id, sampling_id, aux1, aux2, aux3)
        VALUES (%(latitude)s, %(longitude)s, %(datetime)s, %(company_id)s, %(route_id)s, %(truck_id)s, %(truck_name)s, %(duration_interval)s, %(distance)s, %(speed)s, %(status_id)s, %(sampling_id)s, %(aux1)s, %(aux2)s, %(aux3)s)
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/sample')

@app.route('/sample/edit/<string:id>', methods=['POST'])
def edit_sample(id):
    if not session.get('loggedin', False):
        return redirect('login')
    
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT created_at FROM sample WHERE id = %s', (id,))
    created_at = cursor.fetchone()
    cursor.close()

    form_data['id'] = id
    form_data['created_at'] = created_at

    cursor = mysql.connection.cursor()
    query = """
        UPDATE sample SET
        latitude = %(latitude)s,
        longitude = %(longitude)s,
        datetime = %(datetime)s,
        company_id = %(company_id)s,
        route_id = %(route_id)s,
        truck_id = %(truck_id)s,
        truck_name = %(truck_name)s,
        duration_interval = %(duration_interval)s,
        distance = %(distance)s,
        speed = %(speed)s,
        status_id = %(status_id)s,
        sampling_id = %(sampling_id)s,
        created_at = %(created_at)s,
        aux1 = %(aux1)s,
        aux2 = %(aux2)s,
        aux3 = %(aux3)s
        WHERE id = %(id)s
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/sample')

@app.route('/sample/delete', methods=['GET'])
def delete_sample():
    if not session.get('loggedin', False):
        return redirect('login')
    
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM sample WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/sample')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)