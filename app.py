from app import app 

from app.routes import route, truck, sample, identity, identity_company, long_stop, company, sampling, uploaded_file, meals, meal_ingredients, orders, short_stop, order_meals

if __name__ == "__main__":
    app.run(debug = True)
