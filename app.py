from app import app

from app.routes.route import *
from app.routes.truck import *
from app.routes.identity import *
from app.routes.identity_company import *
from app.routes.sampling import *

if __name__ == "__main__":
    app.run(debug = True)
