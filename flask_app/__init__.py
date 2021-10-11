from flask import Flask
from os.path import join, dirname, realpath
import os
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/profile_pics')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
ALLOWED_EXTENSIONS = {'jpeg','jpg','png'}