from app import app

from app.routes.route import *
from app.routes.truck import *

if __name__ == "__main__":
    app.run(debug = True)
