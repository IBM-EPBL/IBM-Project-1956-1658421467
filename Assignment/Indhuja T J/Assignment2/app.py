from flask import Flask, render_template, request, redirect,url_for
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ibm'
mysql=MySQL(app)
@app.route('/')
def Index():
        return render_template('signup.html')
@app.route('/login.html')
def log():
        return render_template('login.html')
@app.route('/profile.html')
def profile():
        return render_template('profile.html')
@app.route('/insert',methods=['POST'])
def insert():
        if request.method=="POST":
            name=request.form['name']
            mail=request.form['email']
            rollno = request.form['rollno']
            password = request.form['password']

            cur=mysql.connection.cursor();
            cur.execute("INSERT INTO user(username,rollno,email,password)VALUES(%s,%s,%s,%s)",(name,rollno,mail,password))
            mysql.connection.commit();

            return redirect(url_for('log'))

@app.route('/authenticate',methods=['POST'])
def authenticate():
    msg=''
    if request.method=="POST":
        uname=request.form['username']
        pwrd=request.form['password']
        cursor1=mysql.connection.cursor()
        cursor1.execute('SELECT * FROM register WHERE name = %s AND pwd = %s', (uname, pwrd,))
        data=cursor1.fetchone()
        if data :
            return render_template('profile.html')
        else:
            msg="Invalid Mail Id/Password"
            return render_template('login.html',msg=msg)

if __name__ == '__main__':
    app.run(debug=True)



