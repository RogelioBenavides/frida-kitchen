from app import app, mysql
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import xml.etree.ElementTree as ET

@app.route('/uploaded_file', methods=['GET','POST'])
def get_uploaded_file():
    if request.method == 'POST':
        id = request.form.get('uploaded_file_id')
        format = request.form.get('format')

        return redirect(url_for('show_uploaded_file', id = id, format = format))
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, filename FROM uploaded_file')
    uploaded_files = cursor.fetchall()
    cursor.close()

    return render_template('uploaded_file.html', uploaded_files = uploaded_files)

@app.route('/uploaded_file/<int:id>&<format>', methods=['GET'])
def show_uploaded_file(id, format):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM uploaded_file WHERE id = %s', (id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"mensaje":"Ruta no encontrada"}), 404
    
    cursor = mysql.connection.cursor()
    cursor.execute('DESCRIBE uploaded_file')
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()

    route_dataJSON = dict(zip(columns, row))

    if format == 'json':
        return jsonify(route_dataJSON)
    elif format == 'xml':
        route_dataXML = ET.Element('uploaded_file')

        for column, value in zip(columns, row):
            ET.SubElement(route_dataXML, column).text = str(value)
        
        response = make_response(ET.tostring(route_dataXML))
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify({"mensaje":"Formato invalido"})
