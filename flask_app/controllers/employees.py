from flask_app import app
from flask_app.models import employee, role, timecard
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import random, yagmail

from dotenv import load_dotenv
load_dotenv()
import os

bcrypt = Bcrypt(app)

def send_email(new_employee):
    body = f"""
    Welcome to Arrays of Sunshine! Here's your registration code: {new_employee.reg_code}
    """
    #print("got here")
    yag = yagmail.SMTP(os.getenv("GMAIL_USERNAME"), oauth2_file="~/oauth2_creds.json")

    #print("and here")
    yag.send(to = new_employee.email, subject = "Arrays of Sunshine - Registration Link", contents = body)
    #print("and lastly here")

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/secret")
# def secret():
#     an_employee = employee.Employee.get_employee_by_email({"email": "antonio@ncstore.biz"})
#     send_email(an_employee)
#     return "hi"

@app.route('/register_employee', methods = ['POST'])
def register_employee():
    data = {
        "email": request.form["reg_email"],
        "reg_code": request.form["reg_code"],
        "password": request.form["reg_password"],
        "confirm_password": request.form["confirm_password"]
    }
    
    if employee.Employee.validate_register_employee(data):
        data["password"] = bcrypt.generate_password_hash(data["password"])
        employee.Employee.register_employee(data)
        registered_employee = employee.Employee.get_employee_by_email(data)
        session["id"] = registered_employee.id
        return redirect("/dashboard")
    
    return redirect("/")

@app.route("/login_employee", methods = ['POST'])
def login_employee():
    data = {
        "email": request.form["login_email"],
        "password": request.form["login_password"]
    }
    if employee.Employee.validate_login_employee(data):
        login_employee = employee.Employee.get_employee_by_email(data)
        session['id'] = login_employee.id
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/reset")
def reset_password_page():
    return render_template("reset_password.html")
    
@app.route("/reset_password", methods=["POST"])
def reset_password():
    data = {
        "email": request.form["email"],
        "password": request.form["password"],
        "confirm_password": request.form["confirm_password"]
    }
    if employee.Employee.validate_reset_password(data):
        pass
    else:
        return redirect("/reset")

    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if not "id" in session:
        return redirect("/")

    today = datetime.now().date()

    week_start = today + timedelta(days = -today.weekday() - 1)
    week_end = today + timedelta(days = 7 - today.weekday()- 2)

    data = {
        "week_start": week_start,
        "week_end": week_end
    }

    all_employees_timecards = timecard.TimeCard.get_timecards_by_week(data)
    worked_employees = []
    total_hours = 0.0
    total_wages = 0.0

    for current_employee in all_employees_timecards:
        current_employee.total_hours = 0.0
        current_employee.total_wages = 0.0
        if len(current_employee.timecards) > 0:
            worked_employees.append(current_employee)
            current_employee.total_hours = 0.0
            for current_timecard in current_employee.timecards:
                total_hours += current_timecard.hours_worked
                current_employee.total_hours += current_timecard.hours_worked
            current_employee.total_wages = float(current_employee.pay_rate) * current_employee.total_hours
            total_wages += current_employee.total_wages

    total_wages = "{:.2f}".format(total_wages)

    #print(all_employees_timecards)
    this_employee = employee.Employee.get_employee_by_id({ "id": session["id"]})
    for current_employee in all_employees_timecards:
        if current_employee.id == this_employee.id:
            this_employee.total_hours = current_employee.total_hours
            this_employee.total_wages = "{:.2f}".format(current_employee.total_wages)
            break

    if this_employee.is_manager == 1:
        return render_template("dashboard_manager.html", logged_in_employee = this_employee, worked_employees = worked_employees, this_week = data, total_hours = total_hours, total_wages = total_wages)
    else:
        return render_template("dashboard_employee.html", logged_in_employee = this_employee, worked_employees = worked_employees, this_week = data)

@app.route("/team/new")
def new_employee():
    if not "id" in session:
        return redirect("/")

    logged_in_employee = employee.Employee.get_employee_by_id({ "id": session["id"] })
    all_roles = role.Role.get_all_roles()

    return render_template("create_employee.html", logged_in_employee=logged_in_employee, all_roles=all_roles)

@app.route("/team/create" , methods = ['POST'])
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

    if employee.Employee.validate_new_employee(data):
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

        data["phone_number"] = data["phone_number"].replace("-", "") if "phone_number" in data else ""

        new_employee_id = employee.Employee.create_employee(data)
        new_employee = employee.Employee.get_employee_by_id({"id": new_employee_id })

        # Send an email to the specified email address with the registration code.
        send_email(new_employee)

        return redirect('/team')
    
    return redirect("/team/new")

@app.route("/team/<int:id>")
def view_employee(id):
    if not "id" in session:
        return redirect("/")

    this_employee = timecard.TimeCard.get_all_time_cards_for_user({"employee_id": id })
    logged_in_employee = employee.Employee.get_employee_by_id({ "id": session["id"] })
    if this_employee.phone_number and len(this_employee.phone_number) == 10:
        this_employee.phone_number = f"{this_employee.phone_number[:3]}-{this_employee.phone_number[3:6]}-{this_employee.phone_number[6:]}"

    this_employee.ytd_hours = 0.0
    for this_timecard in this_employee.timecards:
        # print(this_timecard.date.strftime("%Y"))
        # print(datetime.today().year)
        # print(this_timecard.hours_worked)
        if int(this_timecard.date.strftime("%Y")) == datetime.today().year:
            this_employee.ytd_hours += this_timecard.hours_worked

    this_employee.role = employee.Employee.get_employee_by_id({ "id": id }).role
    if this_employee.avatar_url == None:
        this_employee.avatar_url = "https://www.blexar.com/avatar.png"

    return render_template("view_employee.html", this_employee=this_employee, logged_in_employee=logged_in_employee)

@app.route("/team/<int:id>/edit")
def edit_employee(id):
    if not "id" in session:
        return redirect("/")

    this_employee = employee.Employee.get_employee_by_id({"id": id })
    logged_in_employee = employee.Employee.get_employee_by_id({ "id": session["id"] })
    all_roles = role.Role.get_all_roles()
    if len(this_employee.phone_number) == 10:
        this_employee.phone_number = f"{this_employee.phone_number[:3]}-{this_employee.phone_number[3:6]}-{this_employee.phone_number[6:]}"

    if logged_in_employee.is_manager == 1:
        return render_template("edit_employee_manager_view.html", this_employee=this_employee, logged_in_employee=logged_in_employee, all_roles=all_roles)

    return render_template("edit_employee_employee_view.html", this_employee=this_employee, logged_in_employee=logged_in_employee, all_roles=all_roles)

#Ajax route
@app.route("/team/<int:id>/update", methods = ['POST'])
def update_employee(id):
    if 'id' not in session:
        return redirect("/")

    logged_in_employee = employee.Employee.get_employee_by_id({ "id": session["id"] })
    if logged_in_employee.is_manager == 1:
        data = {
            "id": id,
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "phone_number": request.form["phone_number"],
            "role_id": request.form["role_id"],
            "pay_rate": request.form["pay_rate"],
            "pin_code": request.form["pin_code"],
            "avatar_url": request.form["avatar_url"],
            "birthdate": request.form["birthdate"],
            "is_manager": request.form["is_manager"]
        }
    else:
        data = {
            "id": id,
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "phone_number": request.form["phone_number"],
            "password": request.form["password"],
            "confirm_password": request.form["confirm_password"],
            "avatar_url": request.form["avatar_url"],
            "birthdate": request.form["birthdate"]
        }

    if employee.Employee.validate_update_employee(data):
        this_employee = employee.Employee.get_employee_by_id(data)
        data["phone_number"] = data["phone_number"].replace("-", "") if "phone_number" in data else this_employee.phone_number
        data["role_id"] = int(data["role_id"]) if "role_id" in data else this_employee.role.id
        data["pay_rate"] = float(data["pay_rate"]) if "pay_rate" in data else this_employee.pay_rate
        data["pin_code"] = data["pin_code"] if "pin_code" in data else this_employee.pin_code
        if "password" in data and len(data["password"]) > 7:
            data["password"] = bcrypt.generate_password_hash(data["password"])
        else:
            data["password"] = this_employee.password
        data["status"] = this_employee.status
        data["reg_code"] = this_employee.reg_code
        data["is_manager"] = int(data["is_manager"]) if "is_manager" in data else this_employee.is_manager
        employee.Employee.update_employee(data)
        return redirect(f"/team/{id}")
    return redirect(f"/team/id/edit")


# Ajax route
@app.route("/team/<int:id>/delete")
def delete_employee(id):
    if 'id' not in session:
        return redirect("/")
    data = { "id" : id}
    employee.Employee.delete_employee(data)
    return redirect("/team")

@app.route("/team/<int:id>/terminate")
def terminate_employee(id):
    if not "id" in session:
        return redirect("/")

    data = {"id": id}
    employee.Employee.terminate_employee(data)
    return redirect("/team")

@app.route("/team/<int:id>/rehire")
def rehire_employee(id):
    if not "id" in session:
        return redirect("/")

    data = {"id": id}
    employee.Employee.rehire_employee(data)
    return redirect("/team")

@app.route('/team')
def team_roster():
    if 'id' not in session:
        return redirect("/")
    employees = employee.Employee.get_all_employees()
    current_employee = employee.Employee.get_employee_by_id({ "id": session["id"] })
    roles = role.Role.get_all_roles()

    all_employees = []

    for this_employee in employees:
        if this_employee.status != "HIRED":
            continue
        if len(this_employee.phone_number) == 10:
            this_employee.phone_number = f"{this_employee.phone_number[:3]}-{this_employee.phone_number[3:6]}-{this_employee.phone_number[6:]}"
        all_employees.append(this_employee)

    return render_template('team_roster.html', all_employees = all_employees, current_employee = current_employee, all_roles = roles)
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")