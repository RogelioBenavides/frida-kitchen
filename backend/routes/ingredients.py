from .backend import app, mysql
from flask import redirect, request, render_template

@app.route('/ingredients')
def ingredients():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from ingredients")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC ingredients")
    columns = [column[0] for column in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('ingredients.html', results = results, columns = columns, indices = indices)

@app.route('/ingredients/add', methods=['POST'])
def add_ingredient():
    ingredient_name = request.form['ingredient_name']

    if ingredient_name:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO ingredients (ingredient_name) VALUES (%s)", (ingredient_name,))
        mysql.connection.commit()
        cursor.close()
    return redirect('/ingredients')

@app.route('/ingredients/edit/<string:id>', methods=['POST'])
def edit_ingredient(id):
    ingredient_name = request.form['ingredient_name']

    if ingredient_name:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE ingredients SET ingredient_name = %s WHERE id = %s", (ingredient_name, id))
        mysql.connection.commit()
        cursor.close()
    return redirect('/ingredients')

@app.route('/ingredients/delete', methods=['GET'])
def delete_ingredient():
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM ingredients WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/ingredients')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)