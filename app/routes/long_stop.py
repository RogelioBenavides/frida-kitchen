from app import app, mysql
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import xml.etree.ElementTree as ET

@app.route('/long_stop', methods=['GET','POST'])
def get_long_stops():
    if request.method == 'POST':
        id = request.form.get('long_stop_id')
        format = request.form.get('format')

        return redirect(url_for('show_long_stop', id = id, format = format))
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT created_at, id FROM long_stop')
    long_stops = cursor.fetchall()
    cursor.close()

    return render_template('long_stops.html', long_stops = long_stops)

@app.route('/long_stop/<int:id>&<format>', methods=['GET'])
def show_long_stop(id, format):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM long_stop where id = %s', (id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"mensaje":"Long Stop no encontrada"}), 404
    
    cursor = mysql.connection.cursor()
    cursor.execute('DESCRIBE long_stop')
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()

    dataJSON = dict(zip(columns, row))

    if format == 'json':
        return jsonify(dataJSON)
    elif format == 'xml':
        dataXML = ET.Element('long_stop')

        for column, value in zip(columns, row):
            ET.SubElement(dataXML, column).text = str(value)
        
        response = make_response(ET.tostring(dataXML))
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify({"mensaje":"Formato invalido"})
