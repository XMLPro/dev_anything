# -*- coding: utf-8 -*-
import sqlite3
import os
from contextlib import closing

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('addIncome.html')

@app.route('/add_income')
def add_i():
    return render_template('addIncome.html')

@app.route('/g_add_income')
def g_add_i():
    return render_template('gAddIncome.html')

@app.route('/add_outlay')
def add_o():
    return render_template('addOutlay.html')

@app.route('/g_add_outlay')
def g_add_o():
    return render_template('gAddOutlay.html')

@app.route('/check_income')
def check_i():
    return render_template('checkIncome.html')

@app.route('/g_check_income')
def g_check_i():
    return render_template('gCheckIncome.html')

@app.route('/check_outlay')
def check_o():
    return render_template('check_outlay.html')

@app.route('/g_check_outlay')
def g_check_o():
    return render_template('gCheckOutlay.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/g_login')
def g_login():
    return render_template('gLogin.html')

@app.route('/registered')
def regi():
    return render_template('registered.html')


@app.route('/share_mem')
def share():
    return render_template('shareMem.html')

@app.route('/user_setting')
def u_set():
    return render_template('userSetting.html')

@app.route('/group_setting')
def g_set():
    return render_template('gSetting.html')

@app.route('/add_share_mem')
def asm():
    return render_template('addShareMember.html')

@app.route('/test')
def group():
    return render_template('group.html')

if __name__ == '__main__':
    app.run()
