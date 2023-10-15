from app import app

# Import .py from routes
from app.routes import route, truck, sample, identity, identity_company, long_stop, company, sampling
if __name__ == "__main__":
    app.run(debug = True)
