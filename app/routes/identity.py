from app import app, mysql
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import xml.etree.ElementTree as ET

@app.route('/identity', methods=['GET','POST'])
def get_identity():
    if request.method == 'POST':
        id = request.form.get('identity_id')
        format = request.form.get('format')

        return redirect(url_for('show_identity', id = id, format = format))
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT name, id FROM identity')
    identities = cursor.fetchall()
    cursor.close()

    return render_template('identity.html', identities = identities)

@app.route('/identity/<int:id>&<format>', methods=['GET'])
def show_identity(id, format):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM identity where id = %s', (id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"mensaje":"Ruta no encontrada"}), 404
    
    cursor = mysql.connection.cursor()
    cursor.execute('DESCRIBE identity')
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()

    route_dataJSON = dict(zip(columns, row))

    if format == 'json':
        return jsonify(route_dataJSON)
    elif format == 'xml':
        route_dataXML = ET.Element('identity')

        for column, value in zip(columns, row):
            ET.SubElement(route_dataXML, column).text = str(value)
        
        response = make_response(ET.tostring(route_dataXML))
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify({"mensaje":"Formato invalido"})
