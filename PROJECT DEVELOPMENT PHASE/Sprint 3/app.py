import errno
import os
from flask import Flask, url_for, render_template, request, redirect, session
import requests
import json
from flask_session import Session
import utils


from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SESSION_TYPE = "filesystem"
PERMANENT_SESSION_LIFETIME = 1800


def check_credentials(u, p):
    if utils.getPassword(u) == p:
        session['logged_in'] = True
        session['username'] = u
        print("Valid User")
        return render_template('index.html', name=session['username'])
    return render_template('login.html', error="Invalid Credentials")


def register(u, p, e):
    try:
        r = utils.addUser(u, p, e)
        if (r == "Username Exists"):
            return render_template('signup.html', error="Username Exists")
        return render_template('login.html')
    except:
        return render_template('signup.html', error="Error in inserting user")


def add_finance_record(u, a, c, d, dt):
    try:
        r = utils.createFinanceRecord(u, a, c, d, dt)
        return redirect(url_for('dashboard'))
    except:
        return redirect(url_for('dashboard'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return check_credentials(request.form['username'], request.form['password'])
    else:
        if session.get('logged_in'):
            return redirect(url_for('dashboard'))
        return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        return add_finance_record(request.form['username'], request.form['category'], request.form['amount'], request.form['description'], request.form['date'])
    else:
        if session.get('logged_in'):
            username = session['username']
            rows = utils.fetchFinanceRecord(username)
            return render_template('dashboard.html', rows=rows)
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        return register(request.form['username'], request.form['password'], request.form['email'])
    else:
        return render_template('signup.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


if __name__ == "__main__":
    # app.secret_key = "ThisIsASecretKey"

    db.create_all()
    app.run(host="0.0.0.0", port=8080)
