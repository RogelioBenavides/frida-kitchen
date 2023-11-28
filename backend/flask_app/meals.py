from flask_app import app, mysql
from flask import redirect, request, render_template

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
    file = request.form['image']

    if meal_name and price:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO meals (meal_name, price) VALUES (%s, %s)", (meal_name, price))
        mysql.connection.commit()
        cursor.close()
    return redirect('/meals')

@app.route('/meals/edit/<string:id>', methods=['POST'])
def edit_meal(id):
    meal_name = request.form['meal_name']
    price = request.form['price']

    if meal_name and price:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE meals SET meal_name = %s, price = %s WHERE id = %s", (meal_name, price, id))
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