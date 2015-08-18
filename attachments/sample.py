import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from userManagement import userManagement

DATABASE = 'C:\Users\Owner\PycharmProjects\sample\culuc.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()
    g.userdata = userManagement(g.db)


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        # g.userdata.closeConect


@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash(u'')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if g.userdata.userVerif(request.form['username'],request.form['password']):  # request.form['username'] != app.config['USERNAME']:
            error = u'パスワードかユーザー名が間違ってるのはわかってんだよオイオラァァァァ！！　YO！！'
        else:
            session['logged_in'] = True
            error = u'認証成功'
            # return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash(u'')
    return redirect(url_for('show_entries'))


@app.route('/addUser', methods=['POST'])
def addUser():
    if request.method == 'POST':
        g.userdata.userAdd(request.form['username'], request.form['password'])
    return render_template('addpage.html')


@app.route('/addpage')
def addpage():
    return render_template('addpage.html')


if __name__ == '__main__':
    app.run()
