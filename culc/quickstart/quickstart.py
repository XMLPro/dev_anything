# -*- coding: utf-8 -*-
import sqlite3
from functools import wraps

from flask import Flask, request, session, g, redirect, url_for, render_template

import json
from SpendTableManage import SpendTableManage
from userTableManage import userTableManage
from SNotification import SNotification
from friendManage import friend
from SpendShareManage import SpendShareManage



# 各種設定
DATABASE = 'C:\\Users\\Admin\\PycharmProjects\\culc\\culc.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def reqire_login(f):
    """この関数はラッパ関数です。ログインをしなければアクセスできないようにするための
     制限につかいます。
     基本的には、＠app.route('/')のようにURLを設定した後に
     ＠reqire_loginと入力すると必ずログインしなければアクセスできないようになります。
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        # sessionにlogged_inのキーがなければloginページに飛ばす
        if 'logged_in' not in session or session.get('logged_in') is None:
            return redirect('login')
        else:
            return f(*args, **kwargs)

    return decorated


# database接続
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


# request前にdatebaseにつなげる。
@app.before_request
def before_request():
    g.db = connect_db()
    g.userdata = userTableManage(g.db)
    g.spend = SpendTableManage(g.db)
    g.snoti = SNotification(g.db)
    g.friend = friend(g.db)
    g.share = SpendShareManage(g.db);


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
@reqire_login
def index():
    return render_template('addIncome.html')


@app.route('/add_income')
@reqire_login
def add_i():
    return render_template('addIncome.html')


# 支出入力のページ
@app.route('/add_outlay')
@reqire_login
def add_o():
    return render_template('addOutlay.html')


# 支出追加
@app.route('/add_spend', methods=['POST'])
@reqire_login
def add_spend():
    spend = getattr(g, 'spend', None)
    text = None
    if (request.form['text'] is not "" or request.form['text'] is not None):
        text = request.form['text']
    print(request.form.getlist)

    if spend is not None:
        spend.entryAdd(session.get('username'), request.form['itemName'], request.form['spend'], request.form['day'],
                       request.form['text'])
    return redirect(url_for('add_o'))


# 支出確認
@app.route('/check_outlay')
@reqire_login
def check_o():
    userspend = g.spend.entrySerch(session.get('username'))
    return render_template('check_outlay.html', userspend=userspend)


# 支出更新
@app.route('/update_spend', methods=['POST'])
@reqire_login
def update_spend():
    if request.method == 'POST':
        print(request.form['itemId'])
        print(request.form.getlist('utext'))
        print(request.form.getlist('utext')[0])
        return redirect(url_for('check_o'))


# 支出削除
@app.route('/delete_spend', methods=['POST'])
@reqire_login
def delete_spend():
    if request.method == 'POST':
        g.spend.entryDelete(request.form['itemId'])
        return redirect(url_for('check_o'))


# 支出通知のレンダリング
@app.route('/check_notification')
@reqire_login
def check_no():
    snotiData = g.snoti.entrySerch(session.get('username'))
    return render_template('check_notification.html', snotiData=snotiData)


# 支出通知
@app.route('/addNotification', methods=['POST'])
@reqire_login
def addNotification():
    id = request.form['itemId']
    g.snoti.entryAdd(session.get('username'), request.form['friendName'], g.spend.uniqueSerch(id), id)
    return redirect(url_for('check_o'))


@app.route('/share_spend', methods=['POST'])
@reqire_login
def share_spend():
    data = g.snoti.entryUniqueSerch(request.form['shareId'])
    for e in data:
        g.share.entryAdd(e['sender'], e['recipient'], e['itemName'], e['itemID'])
    g.snoti.entryDelete(request.form['shareId'])
    return redirect(url_for('check_o'))


@app.route('/delete_noti', methods=['POST'])
@reqire_login
def delete_noti():
    g.snoti.entryDelete(request.form['deleteId'])
    return redirect(url_for('check_o'))


# 収入確認
@app.route('/check_income')
@reqire_login
def check_i():
    return render_template('checkIncome.html')


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if g.userdata.entryVerif(request.form['username'], request.form['password']):
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logaut')
def logaut():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('login'))


# ユーザ登録のレンダリング
@app.route('/registered')
def regi():
    return render_template('registered.html')


# ユーザー追加
@app.route('/useradd', methods=['POST'])
def useradd():
    if request.method == 'POST':
        g.userdata.entryAdd(request.form['username'], request.form['password'])
        session['logged_in'] = True
        session['username'] = request.form['username']
        return redirect(url_for('index'))


# 共有設定
@app.route('/share_mem')
@reqire_login
def share():
    return render_template('shareMem.html')


# ユーザー設定
@app.route('/user_setting')
@reqire_login
def u_set():
    return render_template('userSetting.html')


# 共有メンバーの追加
@app.route('/add_share_mem')
@reqire_login
def asm():
    return render_template('addShareMember.html')


# friendのcheck 荒井君担当部分共有機能テストの実装　テスト終了次第削除
@app.route('/check_friend', methods=['GET', 'POST'])
def check_friend():
    # friendデータを取得
    check_fri = g.friend.entrySerch(session.get('username'))
    return render_template('check_friend.html', friend=check_fri)


@app.route('/userValid', methods=['POST',"GET"])
@reqire_login
def check_userVaild():
    result =[request.form["fieldid"],False,"Ok"]
    if (g.user.userValid(request.form['username'])):
        return json.dumps({'','status':'OK','user':user,'pass':password});
    return result

# グループ用の関数または、ページのレンダリング

@app.route('/g_check_outlay')
def g_check_o():
    return render_template('gCheckOutlay.html')


@app.route('/g_add_income')
def g_add_i():
    return render_template('gAddIncome.html')


@app.route('/g_check_income')
def g_check_i():
    return render_template('gCheckIncome.html')


@app.route('/group_setting')
def g_set():
    return render_template('gSetting.html')


@app.route('/g_login')
def g_login():
    return render_template('gLogin.html')


if __name__ == '__main__':
    app.run()
