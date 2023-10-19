from app import app, mysql
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import xml.etree.ElementTree as ET

@app.route('/payments', methods=['GET','POST'])
def get_payments():
    if request.method == 'POST':
        id = request.form.get('payments_id')
        format = request.form.get('format')

        return redirect(url_for('show_payments', id = id, format = format))
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT payment_date, id FROM payments')
    payments = cursor.fetchall()
    cursor.close()

    return render_template('payments.html', payments = payments)

@app.route('/payments/<int:id>&<format>', methods=['GET'])
def show_payments(id, format):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM payments WHERE id = %s', (id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"mensaje":"Pago no encontrada"}), 404
    
    cursor = mysql.connection.cursor()
    cursor.execute('DESCRIBE payments')
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()

    route_dataJSON = dict(zip(columns, row))

    if format == 'json':
        return jsonify(route_dataJSON)
    elif format == 'xml':
        route_dataXML = ET.Element('payments')

        for column, value in zip(columns, row):
            ET.SubElement(route_dataXML, column).text = str(value)
        
        response = make_response(ET.tostring(route_dataXML))
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify({"mensaje":"Formato invalido"})
