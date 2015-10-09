# -*- coding: utf-8 -*-
from flask import render_template, Blueprint, request, redirect, url_for, session
import os, sqlite3

app = Blueprint(__name__, "user")

# USER_LIST = '../users/Users.db'
GROUP_LIST = 'group/Group.db'


@app.route('/')
@app.route('/index')
def index():
    if not os.path.exists(GROUP_LIST):
        create_group_list_db()
    return render_template('gLogin.html')

@app.route('/g_registered')
def g_regi():
    return render_template('gRegistered.html')

@app.route('/creater')
def register_creater():
    return render_template('/user/register_creater.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST' and request.form['user_name'] != "" and request.form['passwd'] != "":
        return do_register(request)
    return render_template('gRegistered.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST' and request.form['user_name'] != "" and request.form['passwd'] != "":
        user_list = sqlite3.connect(GROUP_LIST)
        cur = user_list.cursor()
        data = cur.execute('SELECT pass, creater FROM user_list WHERE name==?', [request.form['user_name']])
        l = data.fetchall()
        print(l)
        if len(l) != 1:
            pass
        elif l[0][0] == request.form['passwd']:
            print("in")
            print(len(l))
            session['user_name'] = request.form['user_name']
            return redirect('/user')
    return render_template('gLogin.html', userFlag=True)


@app.route('/logout')
def logout():
    session.pop('user_name', None)
    return redirect('/')


def do_register(req):
    user_list = sqlite3.connect(GROUP_LIST)
    cur = user_list.cursor()
    data = cur.execute('SELECT name FROM user_list WHERE name==?', [req.form['group_name']])
    if len(data.fetchall()) > 0:
        cur.close()
        return render_template('user/register.html', nameConf=True)
    cur.execute('INSERT OR IGNORE INTO user_list (name, pass) VALUES (?, ?, ?)',
                [req.form['user_name'], req.form['passwd']])
    user_list.commit()
    cur.close()
    session['group_name'] = request.form['group_name']
    return redirect('/')


def create_group_list_db():
    user_list = sqlite3.connect(GROUP_LIST)
    cur = user_list.cursor()
    cur.execute('''CREATE TABLE `user_list` (
                    `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
                    `name`	TEXT,
                    `pass`	TEXT);
                ''')
    user_list.commit()
    cur.close()
