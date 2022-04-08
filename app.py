from flask import Flask, render_template, request, redirect, url_for, send_from_directory, current_app, make_response
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = set(['wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    file_list = os.listdir('data')
    if len(file_list) != 0:
        for i in file_list:
            os.remove('data/'+i)
    return render_template('home.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']

        # check if the post request has the file part
        if 'file' not in request.files or file.filename == '':
            return redirect(url_for('/'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return "invalid file format"
    return render_template('output.html', filename=filename.split('.')[0])


if __name__ == '__main__':
    app.run(debug=True)
