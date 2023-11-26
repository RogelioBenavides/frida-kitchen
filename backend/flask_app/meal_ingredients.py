from flask_app import app, mysql
from flask import redirect, request, render_template

@app.route('/meal_ingredients')
def meal_ingredients():
    # Obtén el número total de registros en la tabla
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) from meal_ingredients")
    total_records = cursor.fetchone()[0]

    # Obtén el número de página actual desde la solicitud del usuario
    page = request.args.get('page', default=1, type=int)

    # Define el número de resultados por página
    per_page = 50  # Número de resultados por página

    # Calcula el número total de páginas
    total_pages = (total_records + per_page - 1) // per_page

    # Calcula el valor de offset
    offset = (page - 1) * per_page

    # Calcula el rango de páginas a mostrar (por ejemplo, 10 páginas)
    page_range = 10
    start_page = max(1, page - (page_range // 2))
    end_page = min(total_pages, start_page + page_range - 1)

    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * from meal_ingredients LIMIT {per_page} OFFSET {offset}")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC meal_ingredients")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("DESC meal_ingredients")
    attribute_types = [attribute_type[1] for attribute_type in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('meal_ingredients.html', results=results, columns=columns, indices=indices, attribute_types=attribute_types, page=page, total_pages=total_pages, start_page=start_page, end_page=end_page)

@app.route('/meal_ingredients/add', methods=['POST'])
def add_meal_ingredients():
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO meal_ingredients (id_ingredient, id_meal, quantity)
        VALUES (%(id_ingredient)s, %(id_meal)s, %(quantity)s)
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/meal_ingredients')

@app.route('/meal_ingredients/edit/<string:id>', methods=['POST'])
def edit_meal_ingredients(id):
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT created_at FROM meal_ingredients WHERE id = %s', (id,))
    created_at = cursor.fetchone()
    cursor.close()

    form_data['id'] = id
    form_data['created_at'] = created_at

    cursor = mysql.connection.cursor()
    query = """
        UPDATE meal_ingredients SET
        id_ingredient = %(id_ingredient)s,
        id_meal = %(id_meal)s,
        quantity = %(quantity)s
        WHERE id = %(id)s
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/meal_ingredients')

@app.route('/meal_ingredients/delete', methods=['GET'])
def delete_meal_ingredients():
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM meal_ingredients WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/meal_ingredients')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)