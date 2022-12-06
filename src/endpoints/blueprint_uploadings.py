from email.policy import strict
import os
from os import mkdir
import time 
from os.path import exists, join
from flask import Blueprint, jsonify, request, current_app, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS

CLASSES = set([
    'Không',
    'Một',
    'Hai',
    'Ba',
    'Bốn',
    'Năm',
    'Bảy',
    'Tám',
    'Chín',
    'Bât',
    'Tắt',
    'Đóng',
    'Mở',
    'Đèn',
    'Quạt'
])

blueprint_uploadings = Blueprint(name="blueprint_uploadings", import_name=__name__)

@blueprint_uploadings.route('/', methods=['POST'], strict_slashes=False)
def post():
    try:
        authorId = request.form['authorId']
        recordings = []
        print(request.files)
        for item in request.files:
            if (item not in CLASSES):
                continue
            class_path = join(current_app.config['DIR'], item)
            if (not exists(class_path)):
                mkdir(class_path)
            file = request.files[item]
            filename = str(int(time.time())) + '.wav'
            filepath = join(class_path, filename)
            file.save(filepath)
            recordings.append((filepath, item))
            
        print(recordings)
    except:
        return ('', 400)
    return ('', 200)

    


