# -*- coding: utf-8 -*-
import sqlite3
from functools import wraps

from flask import Flask, request, session, g, redirect, url_for, render_template

import json
import datetime
import re
from SpendTableManage import SpendTableManage
from userTableManage import userTableManage
from SNotification import SNotification
from friendManage import friend
from SpendShareManage import SpendShareManage
from IncomeTableManage import IncomeTableManage



# 各種設定
DATABASE = 'C:\\Users\\Admin\\PycharmProjects\\culc_M\\culc.db'
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
    g.income = IncomeTableManage(g.db)


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
@reqire_login
def index():
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
        g.spend.entryUpdate(request.form['itemId'], session.get('username'), request.form['uitemName'],
                            request.form['uspend'], request.form['uday'], request.form['utext'])
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


# 収入追加
@app.route('/add_income', methods=['POST'])
@reqire_login
def add_income():
    income = getattr(g, 'income', None)
    if income is not None:
        income.entryAdd(session.get('username'), request.form['itemName'], request.form['spend'], request.form['day'],
                        request.form['text'])
    return redirect(url_for('add_i'))


@app.route('/add_income')
@reqire_login
def add_i():
    return render_template('addIncome.html')


# 統計のページ
@app.route('/jsonToukei')
@reqire_login
def jsonTokei():
    return render_template('jsonToukei.html')


# リクエストを受けたらjsonオブジェクトを返す
@app.route('/jsonGet', methods=['POST'])
@reqire_login
def jsonGet():
    d = datetime.datetime.today()
    strday = str(d.year)
    data = (
        "January, " + strday, "February, " + strday, "March, " + strday, "April, " + strday, "May, " + strday,
        "June, " + strday, "July, " + strday, "August, " + strday, "September, " + strday, "October, " + strday,
        "November, " + strday, "Decembar, " + strday)
    sum = []
    userData = g.spend.entrySerch(session.get('username'))
    jRe = {}
    for p in data:
        sum = 0
        for d in userData:
            if d['day'].find(p) != -1:
                sum += int(d['money'])
        print(sum)
        jRe[p] = sum
    return json.dumps(jRe)


# 収入確認
@app.route('/check_income')
@reqire_login
def check_i():
    userincome = g.income.entrySerch(session.get('username'))
    return render_template('checkIncome.html', userincome=userincome)


# 収入更新
@app.route('/update_income', methods=['POST'])
@reqire_login
def update_income():
    if request.method == 'POST':
        income = getattr(g, 'income', None)
        income.entryUpdate(request.form['uid'], session.get('username'), request.form['uitemName'],
                           request.form['umoney'], request.form['uday'], request.form['utext'])
        return redirect(url_for('check_i'))


# 収入削除
@app.route('/delete_income', methods=['POST'])
@reqire_login
def delete_income():
    if request.method == 'POST':
        g.income.entryDelete(request.form['itemId'])
        return redirect(url_for('check_i'))


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


@app.route('/check_sharespend', methods=['GET'])
def check_sharespend():
    list = []
    check = g.share.entrySerch(session.get('username'))
    for i in check:
        list.extend(g.spend.shareget(i['itemID']))
    for i in list:
        print(i)
        print(i['money'])
    return render_template('check_sharespend.html', list=list)


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
