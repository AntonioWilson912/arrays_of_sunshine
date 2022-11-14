from flask_app import app
from flask_app.models import employee, timecard, timecard_break
from flask import session, redirect, render_template

@app.route("/timecards/new")
def timecard_new_page():
    pass

@app.route("/timecards/<int:timecard_id>")
def view_timecard(timecard_id):
    if not "id" in session:
        return redirect("/")

    timecard_data = {"id": timecard_id}

    this_timecard = timecard.TimeCard.get_timecard(timecard_data)
    this_employee = employee.Employee.get_employee_by_id({"id": session["id"]})
    return render_template("view_timecard.html", this_employee=this_employee, this_timecard=this_timecard)