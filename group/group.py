# -*- coding: utf-8 -*-

from flask import Flask, session, request, redirect, render_template, url_for, g, abort, flash
import os, sqlite3
from contextlib import closing

# 各種設定
DATABASE = 'culc.db' # <- チュートリアルと異なる
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# アプリ生成
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

from contextlib import closing
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# DB接続
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# 各 route() 関数の前に実行される処理
@app.before_request
def before_request():
    # セッションに username が保存されている (= ログイン済み)
    if session.get('username') is not None:
        return
    # リクエストがログインページに関するもの
    if request.path == '/login':
        return
    # ログインされておらずログインページに関するリクエストでもなければリダイレクトする
    return redirect('/login')


@app.route('/', methods=['GET'])
def index():
    # インデックスページを表示する
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # ログイン処理
    if request.method == 'POST':
            # セッションにユーザ名を保存してからインデックスページにリダイレクトする
            session['username'] = request.form['username']
            user = request.form['username']
            password = request.form['password']
            users = (user,password)
            g.db.execute("insert into users (username,password) values (?,?);",users)
            return redirect(url_for('gRegister'))
    # ログインページを表示する
    return render_template('login.html')

@app.route('/glogin', methods=['GET', 'POST'])
def glogin():
    # ログイン処理
    if request.method == 'POST':
            session['groupname'] = request.form['groupname']
            cur = g.db.execute('select title, text from entries order by id desc')
            groups = [dict(groupname=row[0], username=row[1]) for row in cur.fetchall()]
            g.db.commit()
            for group in groups:
                if group.groupname == session['groupname'] and group.username == session['username']:
                    return redirect(url_for('index'))
                    flash('seikou')
                else:
                    session['groupname'] = 'null'
                    return redirect(url_for('glogin'))
                    flash('shippai')
    flash('mawatteru')
    return render_template('gLogin.html')

@app.route('/gRegister', methods=['GET', 'POST'])
def gRegister():
    # ログイン処理
    if request.method == 'POST':
            user = session['username']
            group = request.form['groupname']
            groups =(user,group)
            g.db.execute('insert into groups (username,groupname) values (?,?);',groups)
            g.db.commit()
            return redirect(url_for('glogin'))
    # ログインページを表示する
    return render_template('gRegistered.html')






@app.route('/logout', methods=['GET'])
def logout():
    #セッションからユーザ名を取り除く (ログアウトの状態にする)
    session.pop('username', None)
    # ログインページにリダイレクトする
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)