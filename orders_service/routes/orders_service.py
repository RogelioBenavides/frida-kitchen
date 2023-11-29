from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from datetime import datetime

app = Flask(__name__)

load_dotenv()

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

mysql = MySQL(app)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret" # Change this!
jwt = JWTManager(app)

@app.route('/orders', methods=["GET"])
def get_orders():
    try:
        id_user = request.json.get('id_user', None)

        cursor = mysql.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT orders.id, orders.id_route, orders.created_at,
                   meals.id as meal_id, meals.meal_name, meals.price, order_meals.quantity
            FROM orders
            LEFT JOIN order_meals ON orders.id = order_meals.id_order
            LEFT JOIN meals ON order_meals.id_meal = meals.id
            WHERE orders.id_user = %s
        """, (id_user,))
        
        results = cursor.fetchall()
        cursor.close()

        if len(results) == 0:
            return jsonify({"msg": "Ninguna orden en la lista"}), 401

        orders = {}
        for result in results:
            order_id = result['id']
            if order_id not in orders:
                orders[order_id] = {
                    'id': order_id,
                    'id_route': result['id_route'],
                    'created_at': result['created_at'].isoformat(),
                    'meals': []
                }

            meal_data = {
                'id_meal': result['meal_id'],
                'meal_name': result['meal_name'],
                'price': result['price'],
                'quantity': result['quantity']
            }

            orders[order_id]['meals'].append(meal_data)

        return jsonify({'orders': list(orders.values())}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/orders', methods=["POST"])
def create_order():
    try:
        data = request.get_json()
        print(data)
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO orders (id_route, id_user, created_at)
            VALUES (8634, %s, %s)
        """, (data['id_user'], datetime.utcnow()))
        mysql.connection.commit()
        print('order inserted')

        order_id = cursor.lastrowid

        for meal_data in data.get('cart', []):
            print(meal_data['id_meal'])
            cursor.execute("""
                INSERT INTO order_meals (id_meal, id_order, quantity)
                VALUES (%s, %s, %s)
            """, (meal_data['id_meal'], order_id, meal_data['quantity']))
        
        print('meals inserted')
        
        print(data['payment']['purchase_units'][0]['amount']['value'])

        cursor.execute(
            """INSERT INTO payments (id_order, payment_method, payment_amount, payment_date)
            VALUES (%s, 'PAYPAL', %s, %s)
            """, (order_id, data['payment']['purchase_units'][0]['amount']['value'], datetime.utcnow()))

        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Orden creada exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500