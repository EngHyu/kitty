import os
from flask import *
from werkzeug import secure_filename

UPLOAD_FOLDER = '/Users/roomedia/Desktop/develop/df/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['kitty on keyboard']

        if file is None: pass
        if allowed_file(file.filename) is False: pass

        srcname = secure_filename(file.filename)
        srcname = os.path.join(app.config['UPLOAD_FOLDER'], srcname)
        dstname = os.path.join(app.config['UPLOAD_FOLDER'], "temp." + srcname.split(".")[-1])

        file.save(srcname)
        import kitty
        keyboard = kitty.Keyboard(srcname, dstname)
        os.remove(srcname)

    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
