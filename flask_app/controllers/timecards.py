from flask_app import app
from flask_app.models import employee, timecard, timecard_break
from flask import session, redirect, render_template, request
from datetime import datetime, timedelta

@app.route("/generate_payroll")
def generate_payroll():
    if not "id" in session:
        return redirect("/")

    today = datetime.now().date()

    week_start = today + timedelta(days = -today.weekday() - 1)
    week_end = today + timedelta(days = 7 - today.weekday()- 2)

    data = {
        "week_start": week_start,
        "week_end": week_end
    }

    this_week = f"{week_start} - {week_end}"

    all_employees_timecards = timecard.TimeCard.get_timecards_by_week(data)

    for current_employee in all_employees_timecards:
        current_employee.total_hours = 0.0
        for current_timecard in current_employee.timecards:
            current_employee.total_hours += current_timecard.hours_worked
        current_employee.ot_hours = current_employee.total_hours - 40.0 if current_employee.total_hours > 40.0 else 0.0
        current_employee.ot_rate = float(current_employee.pay_rate) * 1.5
        current_employee.ot_wages = current_employee.ot_hours * current_employee.ot_rate

        regular_hours = current_employee.total_hours if current_employee.total_hours <= 40.0 else current_employee.total_hours - current_employee.ot_hours
        current_employee.regular_wages = "{:.2f}".format(float(current_employee.pay_rate) * regular_hours)
        current_employee.total_wages = "{:.2f}".format(float(current_employee.regular_wages) + float(current_employee.ot_wages))

    return render_template("timesheet_report.html", this_week=this_week, all_employees=all_employees_timecards)

@app.route("/timesheets")
def timesheets():
    if not "id" in session:
        return redirect("/")

    today = datetime.now().date()

    week_start = today + timedelta(days = -today.weekday() - 1)
    week_end = today + timedelta(days = 7 - today.weekday()- 2)

    data = {
        "week_start": week_start,
        "week_end": week_end
    }

    this_week = f"{week_start} - {week_end}"

    all_employees_timecards = timecard.TimeCard.get_timecards_by_week(data)

    for current_employee in all_employees_timecards:
        current_employee.total_hours = 0.0
        for current_timecard in current_employee.timecards:
            current_employee.total_hours += current_timecard.hours_worked
        #print(float(current_employee.pay_rate))
        current_employee.total_wages = "{:.2f}".format(float(current_employee.pay_rate) * current_employee.total_hours)

    #print(all_employees_timecards)
    this_employee = employee.Employee.get_employee_by_id({ "id": session["id"]})

    return render_template("timesheets.html", all_employees = all_employees_timecards, this_employee = this_employee, this_week = this_week)

@app.route("/team/<int:employee_id>/timecards")
def view_employee_timecards(employee_id):
    if not "id" in session:
        return redirect("/")

    this_employee = timecard.TimeCard.get_all_time_cards_for_user({ "employee_id": employee_id })
    this_employee.total_hours = 0.0
    for this_timecard in this_employee.timecards:
        this_employee.total_hours += this_timecard.hours_worked
    this_employee.total_wages = "{:.2f}".format(this_employee.total_hours * float(this_employee.pay_rate))

    logged_in_employee = employee.Employee.get_employee_by_id({ "id": session["id"] })

    return render_template("view_employee_timecards.html", this_employee=this_employee, logged_in_employee=logged_in_employee)

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

    data = {
        "employee_id": employee_id,
        "date": request.form["date"],
        "time_in": request.form["time_in"],
        "time_out": request.form["time_out"]
    }

    if timecard.TimeCard.validate_time_card(data):
        timecard.TimeCard.create_time_card(data)
        return redirect("/timesheets")

    return redirect(f"/team/{employee_id}/timecards/create")

@app.route("/team/<int:employee_id>/timecards/<int:timecard_id>")
def view_timecard(employee_id, timecard_id):
    if not "id" in session:
        return redirect("/")

    timecard_data = {"id": timecard_id }

    this_timecard = timecard.TimeCard.get_timecard(timecard_data)
    this_timecard.time_in = str(this_timecard.time_in)[:5]
    this_timecard.time_out = str(this_timecard.time_out)[:5]
    this_employee = employee.Employee.get_employee_by_id({"id": employee_id})
    logged_in_employee = employee.Employee.get_employee_by_id({"id": session["id"]})
    return render_template("view_timecard.html", this_employee=this_employee, logged_in_employee=logged_in_employee, this_timecard=this_timecard)

@app.route("/team/<int:employee_id>/timecards/<int:timecard_id>/edit")
def edit_timecard(employee_id, timecard_id):
    if not "id" in session:
        return redirect("/")

    timecard_data = {"id": timecard_id }

    this_timecard = timecard.TimeCard.get_timecard(timecard_data)
    this_employee = employee.Employee.get_employee_by_id({"id": employee_id})
    logged_in_employee = employee.Employee.get_employee_by_id({"id": session["id"]})

    return render_template("edit_timecard.html", this_employee=this_employee, logged_in_employee=logged_in_employee, this_timecard=this_timecard)

@app.route("/team/<int:employee_id>/timecards/<int:timecard_id>/update", methods=["POST"])
def update_timecard(employee_id, timecard_id):
    if not "id" in session:
        return redirect("/")

    data = {
        "employee_id": employee_id,
        "timecard_id": timecard_id,
        "date": request.form["date"],
        "time_in": request.form["time_in"],
        "time_out": request.form["time_out"]
    }

    if timecard.TimeCard.validate_existing_time_card(data):
        timecard.TimeCard.update_time_card(data)
        return redirect(f"/team/{employee_id}/timecards/{timecard_id}")

    return redirect(f"/team/{employee_id}/timecards/edit")

@app.route("/team/<int:employee_id>/timecards/<int:timecard_id>/delete")
def delete_timecard(employee_id, timecard_id):
    if not "id" in session:
        return redirect("/")

    data = {
        "id": timecard_id,
    }

    timecard.TimeCard.delete_time_card(data)

    return redirect(f"/team/{employee_id}")

