from .backend import app, mysql
from flask import redirect, request, render_template

@app.route('/route')
def route():
    # Obtén el número total de registros en la tabla
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) from route")
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
    cursor.execute(f"SELECT * from route LIMIT {per_page} OFFSET {offset}")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC route")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("DESC route")
    attribute_types = [attribute_type[1] for attribute_type in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('route.html', results=results, columns=columns, indices=indices, attribute_types=attribute_types, page=page, total_pages=total_pages, start_page=start_page, end_page=end_page)

@app.route('/route/add', methods=['POST'])
def add_route():
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO route (name, beginning_stop_id, end_stop_id, truck_id, distance, average_speed, short_stops_count, time, first_stem_distance, first_stem_time, second_stem_distance, second_stem_time, short_stops_time, traveling_time, stops_between_0_5, stops_between_5_15, stops_between_15_30, stops_between_30_60, stops_between_60_120, stops_between_120_plus, average_short_stop_duration, is_valid, fuel_consumption, aux1, aux2, aux3)
        VALUES (%(name)s, %(beginning_stop_id)s, %(end_stop_id)s, %(truck_id)s, %(distance)s, %(average_speed)s, %(short_stops_count)s, %(time)s, %(first_stem_distance)s, %(first_stem_time)s, %(second_stem_distance)s, %(second_stem_time)s, %(aux1)s, %(traveling_time)s, %(stops_between_0_5)s, %(stops_between_5_15)s, %(stops_between_15_30)s, %(stops_between_30_60)s, %(stops_between_60_120)s, %(stops_between_120_plus)s, %(average_short_stop_duration)s, %(is_valid)s, %(fuel_consumption)s, %(aux1)s, %(aux2)s, %(aux3)s)
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/route')

@app.route('/route/edit/<string:id>', methods=['POST'])
def edit_route(id):
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT created_at FROM route WHERE id = %s', (id,))
    created_at = cursor.fetchone()
    cursor.close()

    form_data['id'] = id
    form_data['created_at'] = created_at

    cursor = mysql.connection.cursor()
    query = """
        UPDATE route SET
        name = %(name)s,
        beginning_stop_id = %(beginning_stop_id)s,
        end_stop_id = %(end_stop_id)s,
        truck_id = %(truck_id)s,
        distance = %(distance)s,
        average_speed = %(average_speed)s,
        short_stops_count = %(short_stops_count)s,
        time = %(time)s,
        first_stem_distance = %(first_stem_distance)s,
        first_stem_time = %(first_stem_time)s,
        second_stem_distance = %(second_stem_distance)s,
        second_stem_time = %(second_stem_time)s,
        short_stops_time = %(short_stops_time)s,
        traveling_time = %(traveling_time)s,
        stops_between_0_5 = %(stops_between_0_5)s,
        stops_between_5_15 = %(stops_between_5_15)s,
        stops_between_15_30 = %(stops_between_15_30)s,
        stops_between_30_60 = %(stops_between_30_60)s,
        stops_between_60_120 = %(stops_between_60_120)s,
        stops_between_120_plus = %(stops_between_120_plus)s,
        average_short_stop_duration = %(average_short_stop_duration)s,
        is_valid = %(is_valid)s,
        fuel_consumption = %(fuel_consumption)s,
        created_at = %(created_at)s,
        aux1 = %(aux1)s,
        aux2 = %(aux2)s,
        aux3 = %(aux3)s
        WHERE id = %(id)s
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/route')

@app.route('/route/delete', methods=['GET'])
def delete_route():
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM route WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/route')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)