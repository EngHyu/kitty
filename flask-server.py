import os
from flask import *
from werkzeug import secure_filename

UPLOAD_FOLDER = '/Users/roomedia/Desktop/develop/df/static'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def getFormat(filename):
    return '.' + filename.split(".")[-1]

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('index.html')

    file = request.files['kitty on keyboard']
    srcname = secure_filename(file.filename)
    srcname = os.path.join(app.config['UPLOAD_FOLDER'], srcname)
    dstname = os.path.join(app.config['UPLOAD_FOLDER'], "temp" + getFormat(srcname))

    file.save(srcname)
    import kitty
    keyboard = kitty.Keyboard(srcname, dstname)
    os.remove(srcname)

    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
