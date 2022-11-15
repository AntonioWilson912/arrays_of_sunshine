from flask_app import app
from flask_app.models import employee, role
from flask import render_template, redirect, request, session, flash

@app.route("/")
def index():
    return render_template("index.html")


#Goes to the page that creates the employee
@app.route("/create-employee-page")
def create_employee_page():
    if 'id' not in session:
        return redirect("/")
    if employee.Employee.validate_is_manager():
        return render_template("create_employee.html")

#Validates that all of the information is inside of the create employee is valid and then registers the employee
@app.route("/create-employee" , methods = ['POST'])
def create_employee():
    if 'id' not in session:
        return redirect("/")
    if employee.Employee.validate_register_employee(request.form):
        employee.Employee.register_employee(request.form)

        return redirect('/manager-dashboard')
    
    return request.referrer

#The route when you click register on the index. It will pop up a page where a user logs in with their email and their
#registration code so that they can input their personal information and set a password.
@app.route("/register-employee-page" , methods = ['POST'])
def register_employee_page():
    if employee.Employee.validate_register_employee_login(request.form):
        registering_employee = employee.Employee.get_employee_by_email(request.form)
        session['id'] = registering_employee.id
        return render_template('register_employee.html', employee = registering_employee)
    
    return request.referrer

#This is the form where the user updates their information. They set a username and password here. 
#From here, they go to the employee dashboard.
@app.route('/register-employee', methods = ['POST'])
def register_employee():
    if 'id' not in session:
        return redirect("/")
    data = { "id" : session['id']}
    employee.Employee.update_employee_registration(request.form)
    user_employee = employee.Employee.get_employee_by_id(data)
    
    
    return redirect("/employee-dashboard", employee = user_employee)


#The route where employees go when they hit login on the index. Takes them to the employee dashboard page.
@app.route("/login-employee", methods = ['POST'])
def login_employee():
    if employee.Employee.validate_login_employee(request.form):
        login_employee = employee.Employee.get_employee_by_email(request.form)
        session['id'] = login_employee.id
        if login_employee.is_manager == 0:
            return redirect("/employee-dashboard")
        if login_employee.is_manager == 1: 
            return redirect("/manager-dashboard")
    else: 
        return request.referrer
    
#The main dashboard for employees that don't have a manager title
@app.route("/employee-dashboard")
def employee_dashboard():
    if 'id' not in session:
        return redirect("/")
    data = { "id" : session['id']}
    employee.Employee.get_employee_by_id(data)
    return render_template('dashboard_employee.html')

#The main dashboard for employees that are managers.
@app.route("/manager-dashboard")
def manager_dashboard():
    if 'id' not in session:
        return redirect("/")
    if employee.Employee.validate_is_manager():
        data = { "id" : session['id']}
        manager = employee.Employee.get_employee_by_id(data)
        employees = employee.Employee.get_all_employees()
        return render_template('dashboard_manager.html', employees = employees , manager = manager )


#Ajax route
@app.route("/employees/<int:id>/edit", methods = ['POST'])
def edit_employee(id):
    if 'id' not in session:
        return redirect("/")
    data = { "id" : id}
    employee.Employee.update_employee(data)
    return 'success', 200


# Ajax route
@app.route("/employees/<int:id>/delete")
def delete_employee(id):
    if 'id' not in session:
        return redirect("/")
    data = { "id" : id}
    employee.Employee.delete_employee(data)
    return "success", 200

@app.route("/employees/<int:id>/terminate")
def terminate_employee(id):
    if not "id" in session:
        return redirect("/")

    data = {"id": id}
    employee.Employee.terminate_employee(data)
    return redirect("/team_roster")

@app.route('/team_roster')
def team_roster():
    if 'id' not in session:
        return redirect("/")
    employees = employee.Employee.get_all_employees()
    return render_template('team_roster.html', employees = employees )
    
    