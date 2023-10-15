from app import app 

# Import .py from routes
from app.routes import *


if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=5000)
