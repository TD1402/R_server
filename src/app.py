"""Flask Application"""

# load libaries
from flask import Flask, jsonify
import sys
from flask_cors import CORS, cross_origin


# load modules
from src.endpoints.blueprint_uploadings import blueprint_uploadings
from src.endpoints.swagger import swagger_ui_blueprint, SWAGGER_URL

# init Flask app
app = Flask(__name__)
CORS(app)

app.config['UPLOAD_EXTENSIONS'] = ['.wav']
app.config['UPLOAD_PATH'] = 'uploads'
app.config['MODEL_PATH'] = 'model'
app.config['DIR'] = 'samples'

# register blueprints. ensure that all paths are versioned!
app.register_blueprint(blueprint_uploadings, url_prefix="/api/speak-submit")

from src.api_spec import spec
# register all swagger documented functions here

with app.test_request_context():
    for fn_name in app.view_functions:
        if fn_name == 'static':
            continue
        print(f"Loading swagger docs for function: {fn_name}")
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)

@app.route("/api/swagger.json")
@cross_origin()

def create_swagger_spec():
    """
    Swagger API definition.
    """
    return jsonify(spec.to_dict())
@app.route("/", methods=["GET"])

def get_example():
    """GET in server"""
    response = jsonify(message="Simple server is running")

    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
