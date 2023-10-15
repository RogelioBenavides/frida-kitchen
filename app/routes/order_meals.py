from app import app, mysql
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import xml.etree.ElementTree as ET

@app.route('/order_meals', methods=['GET','POST'])
def get_order_meals():
    if request.method == 'POST':
        id = request.form.get('order_meals_id')
        format = request.form.get('format')

        return redirect(url_for('show_order_meals', id = id, format = format))
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id FROM order_meals')
    order_meals = cursor.fetchall()
    cursor.close()

    return render_template('order_meals.html', order_meals = order_meals)

@app.route('/order_meals/<int:id>&<format>', methods=['GET'])
def show_order_meals(id, format):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM order_meals WHERE id = %s', (id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"mensaje":"Orden de comida no encontrada"}), 404
    
    cursor = mysql.connection.cursor()
    cursor.execute('DESCRIBE order_meals')
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()

    dataJSON = dict(zip(columns, row))

    if format == 'json':
        return jsonify(dataJSON)
    elif format == 'xml':
        dataXML = ET.Element('order_meals')

        for column, value in zip(columns, row):
            ET.SubElement(dataXML, column).text = str(value)
        
        response = make_response(ET.tostring(dataXML))
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify({"mensaje":"Formato invalido"})