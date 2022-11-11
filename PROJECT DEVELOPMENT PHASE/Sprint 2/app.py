

from flask import Flask, render_template, request


app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home(req):
    if req.method == 'GET':
        return render_template('pages/placeholder.home.html')


@app.route('/dashboard')
def dashboard(req):
    if req.method == 'GET':
        return render_template('pages/dashboard.html')


@app.route('/login')
def login(req):
    if req.method == 'GET':
        return render_template('forms/login.html')


@app.route('/register')
def register(req):
    if req.method == 'GET':
        return render_template('forms/register.html')


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
