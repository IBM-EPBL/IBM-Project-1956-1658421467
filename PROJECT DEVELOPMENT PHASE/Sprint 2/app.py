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


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return check_credentials(request.form['username'], request.form['password'])
    else:
        if session.get('logged_in'):
            return render_template('index.html', name=session['username'])
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
