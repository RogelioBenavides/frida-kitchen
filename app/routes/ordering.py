from app import app, mysql
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import xml.etree.ElementTree as ET
from app.routes import meals as M, ingredients as I

@app.route('/ordering', methods=['GET','POST'])
def ordering():
    if request.method == 'POST':
        id = request.form.get('meals_id')
        format = request.form.get('format')
        quantity = request.form.get('quantity_id')
        #print(M.show_meals(id, format).get_data(as_text=True))
        ordered_meal = M.show_meals(id, format).get_data(as_text=True)

        #address = request.form.get('address')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT meal_name, id FROM meals')
        meals = cursor.fetchall()
        cursor.execute('SELECT price FROM meals WHERE id = %s', (id,))
        unit_price = cursor.fetchall()
        cursor.close()
        print(unit_price[0])
        strin = ""
        strin = strin + unit_price[0]
        total_meal_price = quantity * int(strin)

        return render_template('ordering.html', meals = meals, ordered_meal = ordered_meal, total_meal_price = total_meal_price)
        #return redirect(url_for('show_meals', id = id, format = format))

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT meal_name, id FROM meals')
    meals = cursor.fetchall()
    cursor.close()

    # Muestra ingredientes  show_ingredients
    # Muestra comidas       show_meals
    
    return render_template('ordering.html', meals = meals)
