from app import app, mysql
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import xml.etree.ElementTree as ET

@app.route('/orders', methods=['GET','POST'])
def get_orders():
    if request.method == 'POST':
        id = request.form.get('orders_id')
        format = request.form.get('format')

        return redirect(url_for('show_order', id = id, format = format))
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT created_at, id FROM orders')
    orders = cursor.fetchall()
    cursor.close()

    return render_template('orders.html', orders = orders)

@app.route('/orders/<int:id>&<format>', methods=['GET'])
def show_order(id, format):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM orders WHERE id = %s', (id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"mensaje":"Orden no encontrada"}), 404
    
    cursor = mysql.connection.cursor()
    cursor.execute('DESCRIBE orders')
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()

    dataJSON = dict(zip(columns, row))

    if format == 'json':
        return jsonify(dataJSON)
    elif format == 'xml':
        dataXML = ET.Element('order')

        for column, value in zip(columns, row):
            ET.SubElement(dataXML, column).text = str(value)
        
        response = make_response(ET.tostring(dataXML))
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify({"mensaje":"Formato invalido"})