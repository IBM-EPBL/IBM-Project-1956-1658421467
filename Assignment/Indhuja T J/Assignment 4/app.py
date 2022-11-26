from flask import Flask, request, render_template

app = Flask(__name__)  
 

@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       first_name = request.form.get("fname")
       # getting input with name = lname in HTML form
       last_name = request.form.get("lname")
       age = request.form.get("age")
       # getting input with name = lname in HTML form
       experience = request.form.get("exp")
       return "Your name is "+first_name + last_name
    return render_template("display.html")
 
if __name__=='__main__':
   app.run()