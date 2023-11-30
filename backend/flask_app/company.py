from flask_app import app, mysql
from flask import redirect, request, render_template, session

@app.route('/company')
def company():
    if not session.get('loggedin', False):
        return redirect('login')
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from company")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC company")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("DESC company")
    attribute_types = [attribute_type[1] for attribute_type in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('company.html', results = results, columns = columns, indices = indices, attribute_types = attribute_types)

@app.route('/company/add', methods=['POST'])
def add_company():
    if not session.get('loggedin', False):
        return redirect('login')
    
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO company (name, has_file_in_process, route_count, average_speed, average_trip_distance, average_stem_distance, short_stop_time, traveling_time, resting_time, time_radius_short_stop, distance_radius_short_stop, distance_traveled, average_short_stop_duration, average_trip_duration, average_trip_traveling_time, average_stop_count_per_trip_sd, average_trip_distance_sd, average_stem_distance_sd, average_trip_duration_sd, average_trip_stop_time_sd, average_trip_traveling_time_sd, aux1, aux2, aux3)
        VALUES (%(name)s, %(has_file_in_process)s, %(route_count)s, %(average_speed)s, %(average_stop_count_per_trip)s, %(average_trip_distance)s, %(average_stem_distance)s, %(short_stop_time)s, %(traveling_time)s, %(resting_time)s, %(time_radius_short_stop)s, %(distance_radius_short_stop)s, %(distance_traveled)s, %(average_short_stop_duration)s, %(average_trip_duration)s, %(average_trip_traveling_time)s, %(average_stop_count_per_trip_sd)s, %(average_trip_distance_sd)s, %(average_stem_distance_sd)s, %(average_trip_duration_sd)s, %(average_trip_stop_time_sd)s, %(average_trip_traveling_time_sd)s, %(aux1)s, %(aux2)s, %(aux3)s)
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/company')
    

@app.route('/company/edit/<string:id>', methods=['POST'])
def edit_company(id):
    if not session.get('loggedin', False):
        return redirect('login')
    
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT created_at FROM company WHERE id = %s', (id,))
    created_at = cursor.fetchone()
    cursor.close()

    form_data['id'] = id
    form_data['created_at'] = created_at

    cursor = mysql.connection.cursor()
    query = """
        UPDATE company SET
        name = %(name)s,
        has_file_in_process = %(has_file_in_process)s,
        route_count = %(route_count)s,
        average_speed = %(average_speed)s,
        average_stop_count_per_trip = %(average_stop_count_per_trip)s,
        average_trip_distance = %(average_trip_distance)s,
        average_stem_distance = %(average_stem_distance)s,
        short_stop_time = %(short_stop_time)s,
        traveling_time = %(traveling_time)s,
        resting_time = %(resting_time)s,
        time_radius_short_stop = %(time_radius_short_stop)s,
        distance_radius_short_stop = %(distance_radius_short_stop)s,
        distance_traveled = %(distance_traveled)s,
        average_short_stop_duration = %(average_short_stop_duration)s,
        average_trip_duration = %(average_trip_duration)s,
        average_trip_traveling_time = %(average_trip_traveling_time)s,
        average_stop_count_per_trip_sd = %(average_stop_count_per_trip_sd)s,
        average_trip_distance_sd = %(average_trip_distance_sd)s,
        average_stem_distance_sd = %(average_stem_distance_sd)s,
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
    return redirect('/company')

@app.route('/company/delete', methods=['GET'])
def delete_company():
    if not session.get('loggedin', False):
        return redirect('login')
    
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM company WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/company')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)