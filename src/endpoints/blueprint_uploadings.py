from email.policy import strict
import os
import librosa
from os import mkdir
import time 
from os.path import exists, join
from flask import Blueprint, jsonify, request, current_app, abort
import tensorflow as tf
from werkzeug.utils import secure_filename
from flask_cors import CORS
import numpy as np

SAVED_MODEL_PATH = "model.h5"
SAMPLES_TO_CONSIDER = 22050

SAVED_MODEL_PATH = "saved_model.h5"
SAMPLES_TO_CONSIDER = 22050

class set:
    """Singleton class for keyword spotting inference with trained models.

    :param model: Trained model
    """

    model = None
    _mapping = [
        'Không',
        'Một',
        'Hai',
        'Ba',
        'Bốn',
        'Năm',
        'Bật',
        'Tắt',
        'Đóng',
        'Mở',
        'Đèn',
        'Quạt',
        'Cửa'
    ]
    _instance = None


    def predict(self, file_path):
        """

        :param file_path (str): Path to audio file to predict
        :return predicted_keyword (str): Keyword predicted by the model
        """

        # extract MFCC
        MFCCs = self.preprocess(file_path)

        # we need a 4-dim array to feed to the model for prediction: (# samples, # time steps, # coefficients, 1)
        MFCCs = MFCCs[np.newaxis, ..., np.newaxis]

        # get the predicted label
        predictions = self.model.predict(MFCCs)
        predicted_index = np.argmax(predictions)
        predicted_keyword = self._mapping[predicted_index]
        return predicted_keyword


    def preprocess(self, file_path, num_mfcc=13, n_fft=2048, hop_length=512):
        """Extract MFCCs from audio file.

        :param file_path (str): Path of audio file
        :param num_mfcc (int): # of coefficients to extract
        :param n_fft (int): Interval we consider to apply STFT. Measured in # of samples
        :param hop_length (int): Sliding window for STFT. Measured in # of samples

        :return MFCCs (ndarray): 2-dim array with MFCC data of shape (# time steps, # coefficients)
        """

        # load audio file
        signal, sample_rate = librosa.load(file_path)

        if len(signal) >= SAMPLES_TO_CONSIDER:
            # ensure consistency of the length of the signal
            signal = signal[:SAMPLES_TO_CONSIDER]

            # extract MFCCs
            MFCCs = librosa.feature.mfcc(signal, sample_rate, n_mfcc=num_mfcc, n_fft=n_fft,
                                         hop_length=hop_length)
        return MFCCs.T


def Keyword_Spotting_Service():
    """Factory function for Keyword_Spotting_Service class.

    :return set._instance (_Keyword_Spotting_Service):
    """

    # ensure an instance is created only the first time the factory function is called
    if set._instance is None:
        set._instance = set()
        set.model = tf.keras.models.load_model(SAVED_MODEL_PATH)
    return set._instance


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

