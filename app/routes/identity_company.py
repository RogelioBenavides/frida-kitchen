from app import app, mysql
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import xml.etree.ElementTree as ET

@app.route('/identity_company', methods=['GET','POST'])
def get_identity_company():
    if request.method == 'POST':
        id = request.form.get('identity_company_id')
        format = request.form.get('format')

        return redirect(url_for('show_identity_company', id = id, format = format))
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT IC.id, I.name, C.name FROM identity_company AS IC, identity AS I, company AS C WHERE I.id = IC.id AND C.id = IC.company_id')
    identity_companies = cursor.fetchall()
    cursor.close()

    return render_template('identity_company.html', identity_companies = identity_companies)

@app.route('/identity_company/<int:id>&<format>', methods=['GET'])
def show_identity_company(id, format):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM identity_company where id = %s', (id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"mensaje":"Ruta no encontrada"}), 404
    
    cursor = mysql.connection.cursor()
    cursor.execute('DESCRIBE identity_company')
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()

    route_dataJSON = dict(zip(columns, row))

    if format == 'json':
        return jsonify(route_dataJSON)
    elif format == 'xml':
        route_dataXML = ET.Element('identity_company')

        for column, value in zip(columns, row):
            ET.SubElement(route_dataXML, column).text = str(value)
        
        response = make_response(ET.tostring(route_dataXML))
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify({"mensaje":"Formato invalido"})
