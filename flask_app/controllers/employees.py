from flask_app import app
from flask_app.models import employee, role
from flask import render_template,redirect,request,session,flash

@app.route("/")
def index():
    return "App started!"


@app.route("/register-employee" , methods = ['POST'])
def register_employee():
    pass

@app.route("/login-employee", methods = ['POST'])
def login_employee():
    if employee.validate_login(request.form):
    
        return render_template('')
    pass

@app.route("/delete-employee")
def delete_employee(): 
    pass