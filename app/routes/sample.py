from app import app, mysql
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import xml.etree.ElementTree as ET

@app.route('/sample', methods=['GET','POST'])
def get_sample():
    if request.method == 'POST':
        id = request.form.get('sample_id')
        format = request.form.get('format')

        return redirect(url_for('show_sample', id = id, format = format))
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT truck_name, id FROM sample')
    samples = cursor.fetchall()
    cursor.close()

    return render_template('samples.html', samples = samples)

@app.route('/sample/<int:id>&<format>', methods=['GET'])
def show_sample(id, format):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM sample where id = %s', (id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"mensaje":"Muestra no encontrada"}), 404
    
    cursor = mysql.connection.cursor()
    cursor.execute('DESCRIBE sample')
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()

    sample_dataJSON = dict(zip(columns, row))

    if format == 'json':
        return jsonify(sample_dataJSON)
    elif format == 'xml':
        sample_dataXML = ET.Element('sample')

        for column, value in zip(columns, row):
            ET.SubElement(sample_dataXML, column).text = str(value)
        
        response = make_response(ET.tostring(sample_dataXML))
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify({"mensaje":"Formato invalido"})
