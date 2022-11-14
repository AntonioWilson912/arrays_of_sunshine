from flask_app import app
from flask_app.models import employee, role
from flask import render_template,redirect,request,session,flash

@app.route("/")
def index():
    
    return render_template("index.html")


@app.route("/register-employee-page" , methods = ['POST'])
def register_employee_page():
    if employee.Employee.validate_register_employee_login(request.form):
        registering_employee = employee.Employee.get_employee_by_email(request.form)
        session['id'] = registering_employee.id
        return render_template('register_employee.html', employee = registering_employee)
    
    return request.referrer

@app.route('/register-employee', methods = ['POST'])
def register_employee():
    if 'id' not in session:
        return redirect("/")
    data = { "id" : session['id']}
    employee.Employee.update_employee(request.form)
    user_employee = employee.Employee.get_employee_by_id(data)
    
    
    return redirect("/employee-dashboard", employee = user_employee)

@app.route("/create-employee" , methods = ['POST'])
def create_employee():
    if 'id' not in session:
        return redirect("/")
    if employee.Employee.validate_register_employee(request.form):
        employee.Employee.register_employee(request.form)

        return redirect('/manager-dashboard')
    
    return request.referrer


@app.route("/login-employee", methods = ['POST'])
def login_employee():
    if employee.Employee.validate_login_employee(request.form):
        login_employee = employee.Employee.get_employee_by_email(request.form)
        session['id'] = login_employee.id
        return render_template('dashboard_employee.html', employee = login_employee)
    
    else: 
        return request.referrer
    
@app.route("/employee-dashboard")
def employee_dashboard():
    if 'id' not in session:
        return redirect("/")
    data = { "id" : session['id']}
    employee.Employee.get_employee_by_id(data)
    return render_template('dashboard_employee.html')

@app.route("/manager-dashboard")
def manager_dashboard():
    if 'id' not in session:
        return redirect("/")
    
    employees = employee.Employee.get_all_employees()
    return render_template('dashboard_manager.html', employees = employees )


#Ajax route
@app.route("/edit-employee", methods = ['POST'])
def edit_employee(id):
    if 'id' not in session:
        return redirect("/")
    data = { "id" : id}
    employee.Employee.edit_employee(data)
    return 'success', 200


# Ajax route
@app.route("/delete-employee")
def delete_employee(id):
    if 'id' not in session:
        return redirect("/")
    data = { "id" : id}
    employee.Employee.delete_employee(data)
    return "success", 200


@app.route('/team-roster')
def team_roster():
    if 'id' not in session:
        return redirect("/")
    employees = employee.Employee.get_all_employees()
    return render_template('team_roster.html', employees = employees )
    
    