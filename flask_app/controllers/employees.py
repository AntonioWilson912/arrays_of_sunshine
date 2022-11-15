from flask_app import app
from flask_app.models import employee, role
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
import random

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_admin")
def gen_admin():

    admin = employee.Employee.get_employee_by_id({"id": 1})
    pw_hash = bcrypt.generate_password_hash("password1!")
    data = {
        "id": admin.id,
        "first_name": admin.first_name,
        "last_name": admin.last_name,
        "email": admin.email,
        "password": pw_hash,
        "phone_number": admin.phone_number,
        "birthdate": admin.birthdate,
        "pay_rate": admin.pay_rate,
        "avatar_url": admin.avatar_url,
        "status": admin.status,
        "is_manager": admin.is_manager,
        "pin_code": admin.pin_code,
        "reg_code": admin.reg_code,
        "role_id": admin.role.id
    }
    employee.Employee.update_employee(data)


    return redirect("/")

@app.route("/register_employee_page" , methods = ['POST'])
def register_employee_page():
    if employee.Employee.validate_register_employee_login(request.form):
        registering_employee = employee.Employee.get_employee_by_email(request.form)
        session['id'] = registering_employee.id
        return render_template('register_employee.html', employee = registering_employee)
    
    return request.referrer

@app.route('/register_employee', methods = ['POST'])
def register_employee():
    if 'id' not in session:
        return redirect("/")
    data = { "id" : session['id']}
    employee.Employee.update_employee(request.form)
    user_employee = employee.Employee.get_employee_by_id(data)
    
    
    return redirect("/employee_dashboard", employee = user_employee)

@app.route("/create_employee" , methods = ['POST'])
def create_employee():
    if 'id' not in session:
        return redirect("/")

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "phone_number": request.form["phone_number"],
        "role_id": request.form["role_id"],
    }

    if employee.Employee.validate_register_employee(data):
        all_employees = employee.Employee.get_all_employees()
        all_reg_codes = []
        all_pin_codes = []
        for this_employee in all_employees:
            all_reg_codes.append(this_employee.reg_code)
            all_pin_codes.append(this_employee.pin_code)

        reg_code_not_in_list = False
        while not reg_code_not_in_list:
            new_reg_code = random.randint(100000, 999999)
            if new_reg_code not in all_reg_codes:
                reg_code_not_in_list = True
                data["reg_code"] = new_reg_code

        pin_code_not_in_list = False
        while not pin_code_not_in_list:
            new_pin_code = random.randint(100000, 999999)
            if new_pin_code not in all_pin_codes:
                pin_code_not_in_list = True
                data["pin_code"] = new_pin_code

        employee.Employee.register_employee(data)

        return redirect('/manager_dashboard')
    
    return request.referrer


@app.route("/login_employee", methods = ['POST'])
def login_employee():
    if employee.Employee.validate_login_employee(request.form):
        login_employee = employee.Employee.get_employee_by_email(request.form)
        session['id'] = login_employee.id
        return render_template('dashboard_employee.html', employee = login_employee)
    
    else: 
        return request.referrer

@app.route("/reset")
def reset_password_page():
    return render_template("reset_password.html")
    
@app.route("/reset_password")
def reset_password():
    return redirect("/")

@app.route("/employee_dashboard")
def employee_dashboard():
    if 'id' not in session:
        return redirect("/")
    data = { "id" : session['id']}
    this_employee = employee.Employee.get_employee_by_id(data)
    return render_template('dashboard_employee.html', this_employee=this_employee)

@app.route("/manager_dashboard")
def manager_dashboard():
    if 'id' not in session:
        return redirect("/")
    
    employees = employee.Employee.get_all_employees()
    return render_template('dashboard_manager.html', employees = employees )


#Ajax route
@app.route("/team/<int:id>/edit", methods = ['POST'])
def edit_employee(id):
    if 'id' not in session:
        return redirect("/")
    data = { "id" : id}
    employee.Employee.update_employee(data)
    return 'success', 200


# Ajax route
@app.route("/team/<int:id>/delete")
def delete_employee(id):
    if 'id' not in session:
        return redirect("/")
    data = { "id" : id}
    employee.Employee.delete_employee(data)
    return "success", 200

@app.route("/team/<int:id>/terminate")
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
    roles = role.Role.get_all_roles()
    return render_template('team_roster.html', all_employees = employees, all_roles = roles)
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")