import errno
import os
from flask import Flask, url_for, render_template, request, redirect, session
import requests
import json
from flask_session import Session

# import ibm_db_dbi
# import ibm_db

# cred = open('cred.json')
# cred = json.load(cred)
# conn_str = 'database='+cred['database']+';hostname='+cred['hostname']+';port='+cred['port'] + \
#     ';protocol='+cred['protocol']+';uid=' + \
#     cred['username']+';pwd='+cred['password']
# ibm_db_conn = ibm_db.connect(conn_str, '', '')
# conn = ibm_db_dbi.Connection(ibm_db_conn)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SESSION_TYPE = "filesystem"
PERMANENT_SESSION_LIFETIME = 1800

app.config.update(SECRET_KEY=os.urandom(24))

app.config.from_object(__name__)
Session(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
db.init_app(app)
with app.app_context():
    db.create_all()


class User(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    roll = db.Column(db.String(100))

    def __init__(self, username, password, email, roll):
        self.username = username
        self.password = password
        self.email = email
        self.roll = roll


def check_credentials(u, p):
    data = User.query.filter_by(username=u, password=p).first()
    if data is not None:
        session['logged_in'] = True
        session['username'] = u
        return render_template('index.html', name=session['username'])
        # return True
    # print("Checking password from db")
    # return False
    return render_template('login.html', error="Invalid Credentials")


def register(u, p, e, r):
    try:
        db.session.add(
            User(username=u, password=p, email=e, roll=r))
        db.session.commit()
        return render_template('login.html')

    except:
        print("Error in inserting user")
    return render_template('signup.html', error="Account Already Exists")

    return False
    # print("Registering user")
    # return True


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
        return register(request.form['username'], request.form['password'], request.form['email'], request.form['roll'])
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
