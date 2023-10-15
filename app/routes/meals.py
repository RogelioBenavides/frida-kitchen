from app import app, mysql
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import xml.etree.ElementTree as ET

@app.route('/meals', methods=['GET','POST'])
def get_meals():
    if request.method == 'POST':
        id = request.form.get('meals_id')
        format = request.form.get('format')

        return redirect(url_for('show_meals', id = id, format = format))
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT meal_name, id FROM meals')
    meals = cursor.fetchall()
    cursor.close()

    return render_template('meals.html', meals = meals)

@app.route('/meals/<int:id>&<format>', methods=['GET'])
def show_meals(id, format):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM meals WHERE id = %s', (id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"mensaje":"Receta no encontrada"}), 404
    
    cursor = mysql.connection.cursor()
    cursor.execute('DESCRIBE meals')
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()

    route_dataJSON = dict(zip(columns, row))

    if format == 'json':
        return jsonify(route_dataJSON)
    elif format == 'xml':
        route_dataXML = ET.Element('meals')

        for column, value in zip(columns, row):
            ET.SubElement(route_dataXML, column).text = str(value)
        
        response = make_response(ET.tostring(route_dataXML))
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify({"mensaje":"Formato invalido"})
