from flask_app import app
from flask_app.models import employee, timecard, timecard_break
from flask import session, redirect, render_template

@app.route("/timesheets")
def all_timesheets():
    if not "id" in session:
        return redirect("/")

    return render_template("timesheets.html")

@app.route("/team/<int:employee_id>/timecards/new")
def timecard_new_page(employee_id):
    if not "id" in session:
        return redirect("/")
    this_employee = employee.Employee.get_employee_by_id({"id": employee_id})
    current_employee = employee.Employee.get_employee_by_id({"id": session["id"]})
    return render_template("create_timecard.html", current_employee = current_employee, this_employee = this_employee)

@app.route("/team/<int:employee_id>/timecards/create", methods=["POST"])
def create_timecard(employee_id):
    if not "id" in session:
        return redirect("/")

    return redirect("/timesheets")

@app.route("/team/<int:employee_id>/timecards/<int:timecard_id>")
def view_timecard(timecard_id):
    if not "id" in session:
        return redirect("/")

    timecard_data = {"id": timecard_id}

    this_timecard = timecard.TimeCard.get_timecard(timecard_data)
    this_employee = employee.Employee.get_employee_by_id({"id": session["id"]})
    return render_template("view_timecard.html", this_employee=this_employee, this_timecard=this_timecard)