from app import app, mysql
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import xml.etree.ElementTree as ET

@app.route('/camiones', methods=['GET','POST'])
def get_truck():
    if request.method == 'POST':
        id = request.form.get('truck_id')
        format = request.form.get('format')

        return redirect(url_for('show_truck', id = id, format = format))
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT name, id FROM truck')
    trucks = cursor.fetchall()
    cursor.close()

    return render_template('trucks.html', trucks = trucks)

@app.route('/camion/<int:id>&<format>', methods=['GET'])
def show_truck(id, format):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM truck where id = %s', (id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"mensaje":"Camion no encontrada"}), 404
    
    cursor = mysql.connection.cursor()
    cursor.execute('DESCRIBE truck')
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()

    truck_dataJSON = dict(zip(columns, row))

    if format == 'json':
        return jsonify(truck_dataJSON)
    elif format == 'xml':
        truck_dataXML = ET.Element('truck')

        for column, value in zip(columns, row):
            ET.SubElement(truck_dataXML, column).text = str(value)
        
        response = make_response(ET.tostring(truck_dataXML))
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify({"mensaje":"Formato invalido"})
