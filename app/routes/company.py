from app import app, mysql
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import xml.etree.ElementTree as ET

@app.route('/company', methods=['GET','POST'])
def get_company():
    if request.method == 'POST':
        id = request.form.get('company_id')
        format = request.form.get('format')

        return redirect(url_for('show_company', id = id, format = format))
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT name, id FROM company')
    companies = cursor.fetchall()
    cursor.close()

    return render_template('company.html', companies = companies)

@app.route('/company/<int:id>&<format>', methods=['GET'])
def show_company(id, format):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM company where id = %s', (id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"mensaje":"Ruta no encontrada"}), 404
    
    cursor = mysql.connection.cursor()
    cursor.execute('DESCRIBE company')
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()

    route_dataJSON = dict(zip(columns, row))

    if format == 'json':
        return jsonify(route_dataJSON)
    elif format == 'xml':
        route_dataXML = ET.Element('company')

        for column, value in zip(columns, row):
            ET.SubElement(route_dataXML, column).text = str(value)
        
        response = make_response(ET.tostring(route_dataXML))
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify({"mensaje":"Formato invalido"})
