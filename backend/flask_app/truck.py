from flask_app import app, mysql
from flask import redirect, request, render_template, session

@app.route('/truck')
def truck():
    if not session.get('loggedin', False):
        return redirect('login')
    
    # Obtén el número total de registros en la tabla
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) from truck")
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
    cursor.execute(f"SELECT * from truck LIMIT {per_page} OFFSET {offset}")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC truck")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("DESC truck")
    attribute_types = [attribute_type[1] for attribute_type in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('truck.html', results=results, columns=columns, indices=indices, attribute_types=attribute_types, page=page, total_pages=total_pages, start_page=start_page, end_page=end_page)

@app.route('/truck/add', methods=['POST'])
def add_truck():
    if not session.get('loggedin', False):
        return redirect('login')
    
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO truck (name, company_id, total_distance, route_count, average_duration, average_speed, average_stop_count_per_trip, average_distance_between_short_stops, average_stem_distance, average_trip_distance, short_stops_time, traveling_time, resting_time, stops_between_0_5, stops_between_5_15, stops_between_15_30, stops_between_30_60, stops_between_60_120, stops_between_120_plus, average_trip_stop_time, average_trip_traveling_time, average_stop_count_per_trip_sd,average_trip_distance_sd, average_stem_distance_sd, average_speed_sd, average_trip_duration_sd, average_trip_stop_time_sd, average_trip_traveling_time_sd,aux1, aux2, aux3)
        VALUES (%(name)s, %(company_id)s, %(total_distance)s, %(route_count)s, %(average_duration)s, %(average_speed)s, %(average_stop_count_per_trip)s, %(average_distance_between_short_stops)s, %(average_stem_distance)s, %(average_trip_distance)s, %(short_stops_time)s, %(traveling_time)s, %(resting_time)s %(stops_between_0_5)s, %(stops_between_5_15)s, %(stops_between_15_30)s, %(stops_between_30_60)s, %(stops_between_60_120)s, %(stops_between_120_plus)s, %(average_trip_stop_time)s, %(average_trip_traveling_time)s, %(average_stop_count_per_trip_sd)s, %(average_trip_distance_sd)s, %(average_stem_distance_sd)s, %(average_speed_sd)s, %(average_trip_duration_sd)s, %(average_trip_stop_time_sd)s, %(average_trip_traveling_time_sd)s, %(aux1)s, %(aux2)s, %(aux3)s)
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/truck')

@app.route('/truck/edit/<string:id>', methods=['POST'])
def edit_truck(id):
    if not session.get('loggedin', False):
        return redirect('login')
    
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT created_at FROM truck WHERE id = %s', (id,))
    created_at = cursor.fetchone()
    cursor.close()

    form_data['id'] = id
    form_data['created_at'] = created_at

    cursor = mysql.connection.cursor()
    query = """
        UPDATE truck SET
        name = %(name)s,
        company_id = %(company_id)s,
        total_distance = %(total_distance)s,
        route_count = %(route_count)s,
        average_duration = %(average_duration)s,
        average_speed = %(average_speed)s,
        average_stop_count_per_trip = %(average_stop_count_per_trip)s,
        average_distance_between_short_stops = %(average_distance_between_short_stops)s,
        average_stem_distance = %(average_stem_distance)s,
        average_trip_distance = %(average_trip_distance)s,
        short_stops_time = %(short_stops_time)s,
        traveling_time = %(traveling_time)s,
        resting_time = %(resting_time)s,
        stops_between_0_5 = %(stops_between_0_5)s,
        stops_between_5_15 = %(stops_between_5_15)s,
        stops_between_15_30 = %(stops_between_15_30)s,
        stops_between_30_60 = %(stops_between_30_60)s,
        stops_between_60_120 = %(stops_between_60_120)s,
        stops_between_120_plus = %(stops_between_120_plus)s,
        average_trip_stop_time = %(average_trip_stop_time)s,
        average_trip_traveling_time = %(average_trip_traveling_time)s,
        average_stop_count_per_trip_sd = %(average_stop_count_per_trip_sd)s,
        average_trip_distance_sd = %(average_trip_distance_sd)s,
        average_stem_distance_sd = %(average_stem_distance_sd)s,
        average_speed_sd = %(average_speed_sd)s,
        average_trip_duration_sd = %(average_trip_duration_sd)s,
        average_trip_stop_time_sd = %(average_trip_stop_time_sd)s,
        average_trip_traveling_time_sd = %(average_trip_traveling_time_sd)s,
        created_at = %(created_at)s,
        aux1 = %(aux1)s,
        aux2 = %(aux2)s,
        aux3 = %(aux3)s
        WHERE id = %(id)s
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/truck')

@app.route('/truck/delete', methods=['GET'])
def delete_truck():
    if not session.get('loggedin', False):
        return redirect('login')
    
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM truck WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/truck')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)