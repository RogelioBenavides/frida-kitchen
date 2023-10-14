from app import app 

from app.routes.route import *
from app.routes.truck import *
from app.routes.sample import *
from app.routes.identity import *
from app.routes.identity_company import *
from app.routes.company import *

if __name__ == "__main__":
    app.run(debug = True)
