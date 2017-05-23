from flask import *

UPLOAD_FOLDER = '/Users/roomedia/Desktop/develop/df/static'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        import os
        import kitty
        from werkzeug import secure_filename

        file = request.files['kitty on keyboard']
        srcname = secure_filename(file.filename)
        srcname = os.path.join(app.config['UPLOAD_FOLDER'], srcname)
        dstname = os.path.join(app.config['UPLOAD_FOLDER'], "temp.jpg")

        file.save(srcname)
        keyboard = kitty.Keyboard(srcname, dstname)
        os.remove(srcname)

    return render_template('index.html')



@app.route('/input', methods=['GET', 'POST'])
def input():
    messages = ['test1', 'test2', 'test3']
    if request.method == 'POST':
        import typing
        message = request.form['message']
        messages.append(message)
        typing.Spliter(message)

    return render_template('input.html', messages=messages)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
