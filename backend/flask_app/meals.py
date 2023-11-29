from flask_app import app, mysql
from flask import redirect, request, render_template, jsonify
from PIL import Image
import base64
import io
import requests
import json
import os

@app.route('/meals')
def meals():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from meals")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC meals")
    columns = [column[0] for column in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('meals.html', results = results, columns = columns, indices = indices)

@app.route('/meals/add', methods=['POST'])
def add_meal():
    # Getting the form fields
    meal_name = request.form['meal_name']
    price = request.form['price']
    description = request.form['description']
    file = request.files['image']

    # Checking if the image is valid
    try:
        img = Image.open(file.stream)
        img.verify()
    except Exception as e:
        print(e)
        return redirect('/meals') # Leave with no changes

    # Upload Image to IMGGB
    api_url = "https://api.imgbb.com/1/upload"

    img = Image.open(file.stream)

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes = img_bytes.getvalue()

    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    params = {"key":os.environ.get('IMGBB_KEY'),
              "image": img_base64}
    
    response = requests.post(api_url, params)
    response = json.loads(response.text)

    saved_img_url = response["data"]["url"]

    if meal_name and price and description and img and saved_img_url:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO meals (meal_name, price, description, image_url) VALUES (%s, %s, %s, %s)", (meal_name, price, description, saved_img_url))
        mysql.connection.commit()
        cursor.close()

    return redirect('/meals')

@app.route('/meals/edit/<string:id>', methods=['POST'])
def edit_meal(id):
    meal_name = request.form['meal_name']
    price = request.form['price']
    description = request.form['description']

    if not request.files['image']:
        if meal_name and price and description:
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE meals SET meal_name = %s, price = %s, description = %s WHERE id = %s", (meal_name, price, description, id))
            mysql.connection.commit()
            cursor.close()
            return redirect('/meals')
        
    file = request.files['image']

    # Checking if the image is valid
    try:
        img = Image.open(file.stream)
        img.verify()
    except Exception as e:
        print(e)
        return redirect('/meals') # Leave with no changes

    # Upload Image to IMGGB
    api_url = "https://api.imgbb.com/1/upload"

    img = Image.open(file.stream)

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes = img_bytes.getvalue()

    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    params = {"key":os.environ.get('IMGBB_KEY'),
              "image": img_base64}
    
    response = requests.post(api_url, params)
    response = json.loads(response.text)

    saved_img_url = response["data"]["url"]

    if meal_name and price and description and img and saved_img_url:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE meals SET meal_name = %s, price = %s, description = %s, image_url = %s WHERE id = %s", (meal_name, price, description, saved_img_url, id))
        mysql.connection.commit()
        cursor.close()

    return redirect('/meals')
        
    

@app.route('/meals/delete', methods=['GET'])
def delete_meal():
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM meals WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/meals')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)