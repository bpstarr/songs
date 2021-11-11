from flask import Flask
from os.path import join, dirname, realpath
import os, logging
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/profile_pics')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
ALLOWED_EXTENSIONS = {'jpeg','jpg','png'}
logging.basicConfig(filename = 'record.log', level = logging.DEBUG, format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
@app.route('/blogs')
def blog():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return f"Welcome to the Blog"