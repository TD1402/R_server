"""Web Server Gateway Interface"""

##################
# FOR PRODUCTION
####################
from src.app import app
from flask_cors import CORS
if __name__ == "__main__":
    ####################
    # FOR DEVELOPMENT
    ####################
    app.run(host='0.0.0.0', debug=True)

