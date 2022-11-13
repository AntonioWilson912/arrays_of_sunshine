from flask_app import app
from flask_app.models import employee, role
from flask import render_template,redirect,request,session,flash

@app.route("/")
def index():
    
    return render_template("index.html")


@app.route("/register-employee" , methods = ['POST'])
def register_employee():
    if employee.Employee.validate_register_employee(request.form):
        employee.Employee.create_employee(request.form)
        session['id'] = employee.Employee.id
        return render_template('dashboard_employee.html', employee = employee.Employee)
    
    return request.referrer


@app.route("/login-employee", methods = ['POST'])
def login_employee():
    if employee.Employee.validate_login_employee(request.form):
        employee.Employee.get_employee_by_email(request.form)
        session['id'] = employee.Employee.id
        return render_template('dashboard_employee.html', employee = employee.Employee)
    
    else: 
        return request.referrer


@app.route("/edit-employee", methods = ['POST'])
def edit_employee(id):
    if 'id' not in session:
        return redirect("/")
    data = { "id" : id}
    employee.Employee.delete_employee(data)
    

@app.route("/delete-employee")
def delete_employee(id):
    if 'id' not in session:
        return redirect("/")
    data = { "id" : id}
    employee.Employee.delete_employee(data)
    
    return "success", 200