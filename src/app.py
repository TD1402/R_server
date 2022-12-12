"""Flask Application"""

from __future__ import division, print_function
import random
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
import h5py
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer


# load libaries
from flask import Flask, jsonify
import sys
from flask_cors import CORS, cross_origin


# load modules
from src.endpoints.blueprint_uploadings import blueprint_uploadings
from src.endpoints.swagger import swagger_ui_blueprint, SWAGGER_URL


import librosa

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



# file_part=os.path.dirname("./models")+"./models/saved_model.h5"

MODEL_PATH ="G:/recording-server-master/src/models/saved_model.h5"

# Load your trained model
model = load_model(MODEL_PATH)
# model.predict()    


@app.route("/predict", methods=["POST"])
def predict():
	"""Endpoint to predict keyword
    :return (json): This endpoint returns a json file with the following format:
        {
            "keyword": "down"
        }
	"""
	# get file from POST request and save it
	audio_file = request.files["file"]
	file_name = str(random.randint(0, 100000))
	audio_file.save(file_name)

	# instantiate keyword spotting service singleton and get prediction
	kss =blueprint_uploadings.Keyword_Spotting_Service()
	predicted_keyword = kss.predict(file_name)

	# we don't need the audio file any more - let's delete it!
	os.remove(file_name)

	# send back result as a json file
	result = {"keyword": predicted_keyword}
	return jsonify(result)

# print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
#from keras.applications.resnet50 import ResNet50
#model = ResNet50(weights='imagenet')
#model.save('')
print('Model loaded. Check http://127.0.0.1:5000/')

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
