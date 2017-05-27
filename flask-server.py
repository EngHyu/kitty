import os
import sqlite3
from flask import *
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

UPLOAD_FOLDER = os.path.abspath('.')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DATABASE = '/Users/roomedia/Desktop/develop/df/sqlite3/database.db'

oauth = OAuth(app)

twitter = oauth.remote_app(
    'twitter',
    consumer_key='xBeXxg9lyElUgwZT6AZ0A',
    consumer_secret='aawnSpNTOVuDCjx7HMh6uSXetjNN8zWLpZwCEU4LBrk',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize'
)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=(), one=False):
    cursor = get_db().execute(query, args)
    row_values = cursor.fetchall()
    cursor.close()
    return (row_values[0] if row_values else None) if one else row_values


def commit_db():
    get_db().commit()


def delete_message_db(message_id, user_id):
    query = 'delete from message where message.user_id is %s and message.id is %s;' % (user_id, message_id)
    query_db(query)
    commit_db()


@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


@app.before_request
def before_request():
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']
        get_messages()


def get_messages():
    query = 'select * from message where message.user_id is %s;' % (g.user['user_id'])
    g.messages = [message for message in query_db(query)]


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if g.user is None:
        return render_template('pre-login.html')

    if g.user is not None:
        return render_template('post-login.html', user=g.user['user_id'])


@app.route('/login/')
def login():
    callback_url = url_for('oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)


@app.route('/oauthorized/')
def oauthorized():
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
        before_request()

        query = 'select * from user where user.id is "%s";' % (g.user['user_id'])
        if query_db(query) == list():
            query = 'insert into user values(%s, "%s");' % (g.user['user_id'], 'twitter')
            query_db(query)
            commit_db()

    return redirect(url_for('index'))


@app.route('/logout/')
def logout():
    session.pop('twitter_oauth', None)
    return redirect(url_for('index'))


@app.route('/devices/', methods=['GET', 'POST'])
def devices():
    if g.user is None:
        return redirect(url_for('login', next=request.url))

    import kitty
    from werkzeug import secure_filename

    if request.method == 'POST':
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'sqlite3', g.user['user_id'])
        if not os.path.exists(path):
            os.mkdir(path)

        file = request.files['img-kitty-keyboard']
        srcname = secure_filename(file.filename)
        srcname = os.path.join(path, srcname)
        file.save(srcname)

        query = 'SELECT id FROM keyboard WHERE keyboard.user_id is %s ORDER BY id DESC;' % (g.user['user_id'])
        keyboard_ids = query_db(query)
        print(keyboard_ids)
        #'SELECT id FROM keyboard ORDER BY id DESC WHERE keyboard.user_id is %s;'

        keyboard_id  = keyboard_ids[-1] + 1 if keyboard_ids != list() else 0
        keyboard = kitty.Keyboard(path, keyboard_id, srcname)
        os.remove(srcname)

    return render_template('devices.html')


@app.route('/send/', methods=['GET', 'POST'])
def send():
    if g.user is None:
        return redirect(url_for('login', next=request.url))

    if request.method == 'POST':
        import typing
        message = request.form['message']
        message_id = 0 if g.messages == list() else g.messages[-1][0] + 1
        #typing.Spliter(message)

        query = 'insert into message values(%d, "%s", "%s");' % (message_id, g.user['user_id'], message);
        query_db(query)
        commit_db()

    get_messages()
    return render_template('send.html', messages=g.messages)


@app.route('/send/delete/', methods=['POST'])
def send_delete():
    delete_message_db(request.form['id'], g.user['user_id'])
    return redirect(url_for('send'))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
