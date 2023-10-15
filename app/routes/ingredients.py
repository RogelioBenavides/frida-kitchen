from app import app, mysql
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import xml.etree.ElementTree as ET

@app.route('/ingredients', methods=['GET','POST'])
def get_ingredients():
    if request.method == 'POST':
        id = request.form.get('ingredients_id')
        format = request.form.get('format')

        return redirect(url_for('show_ingredients', id = id, format = format))
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT ingredient_name, id FROM ingredients')
    ingredients = cursor.fetchall()
    cursor.close()

    return render_template('ingredients.html', ingredients = ingredients)

@app.route('/ingredients/<int:id>&<format>', methods=['GET'])
def show_ingredients(id, format):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM ingredients WHERE id = %s', (id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"mensaje":"Ingrediente no encontrado"}), 404
    
    cursor = mysql.connection.cursor()
    cursor.execute('DESCRIBE ingredients')
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()

    route_dataJSON = dict(zip(columns, row))

    if format == 'json':
        return jsonify(route_dataJSON)
    elif format == 'xml':
        route_dataXML = ET.Element('ingredients')

        for column, value in zip(columns, row):
            ET.SubElement(route_dataXML, column).text = str(value)
        
        response = make_response(ET.tostring(route_dataXML))
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify({"mensaje":"Formato invalido"})
