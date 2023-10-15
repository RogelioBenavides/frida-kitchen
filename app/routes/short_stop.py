from app import app, mysql
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import xml.etree.ElementTree as ET

@app.route('/short_stop', methods=['GET','POST'])
def get_short_stop():
    if request.method == 'POST':
        id = request.form.get('short_stop_id')
        format = request.form.get('format')

        return redirect(url_for('show_short_stop', id = id, format = format))
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, created_at FROM short_stop')
    short_stops = cursor.fetchall()
    cursor.close()

    return render_template('short_stop.html', short_stops = short_stops)

@app.route('/short_stop/<int:id>&<format>', methods=['GET'])
def show_short_stop(id, format):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM short_stop WHERE id = %s', (id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"mensaje":"Short stop no encontrada"}), 404
    
    cursor = mysql.connection.cursor()
    cursor.execute('DESCRIBE short_stop')
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()

    dataJSON = dict(zip(columns, row))

    if format == 'json':
        return jsonify(dataJSON)
    elif format == 'xml':
        dataXML = ET.Element('short_stop')

        for column, value in zip(columns, row):
            ET.SubElement(dataXML, column).text = str(value)
        
        response = make_response(ET.tostring(dataXML))
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify({"mensaje":"Formato invalido"})
