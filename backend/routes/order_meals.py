from .backend import app, mysql
from flask import redirect, request, render_template

@app.route('/order_meals')
def order_meals():
    # Obtén el número total de registros en la tabla
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) from order_meals")
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
    cursor.execute(f"SELECT * from order_meals LIMIT {per_page} OFFSET {offset}")
    results = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("DESC order_meals")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("DESC order_meals")
    attribute_types = [attribute_type[1] for attribute_type in cursor.fetchall()]

    indices = list(range(len(columns)))

    return render_template('order_meals.html', results=results, columns=columns, indices=indices, attribute_types=attribute_types, page=page, total_pages=total_pages, start_page=start_page, end_page=end_page)

@app.route('/order_meals/add', methods=['POST'])
def add_order_meals():
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO order_meals (id_meal, id_order, quantity)
        VALUES (%(id_meal)s, %(id_order)s, %(quantity)s)
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/order_meals')

@app.route('/order_meals/edit/<string:id>', methods=['POST'])
def edit_order_meals(id):
    form_data = request.form.to_dict(flat=True)

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT created_at FROM order_meals WHERE id = %s', (id,))
    created_at = cursor.fetchone()
    cursor.close()

    form_data['id'] = id
    form_data['created_at'] = created_at

    cursor = mysql.connection.cursor()
    query = """
        UPDATE order_meals SET
        id_meal = %(id_meal)s,
        id_order = %(id_order)s,
        quantity = %(quantity)s
        WHERE id = %(id)s
    """
    cursor.execute(query, form_data)
    mysql.connection.commit()
    cursor.close()
    return redirect('/order_meals')

@app.route('/order_meals/delete', methods=['GET'])
def delete_order_meals():
    id_to_delete = request.args.get('id')
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM order_meals WHERE id = %s', (id_to_delete,))
        mysql.connection.commit()
        cursor.close()

        return redirect('/order_meals')
    except Exception as e:
        return "Error al eliminar el registro: " + str(e)