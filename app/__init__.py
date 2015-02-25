import os
from flask import Flask

UPLOAD_FOLDER = os.path.join(os.path.realpath(__file__) , '/tmp/')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] =  2 * 1024 * 1024
from app import views
