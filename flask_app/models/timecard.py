from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import employee
from flask import flash

class TimeCard:

    db_name = "arrays_of_sunshine"

    def __init__(self, data):
        self.id = data["id"]
        self.date = data["date"]
        self.time_in = data["time_in"]
        self.time_out = data["time_out"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.employee = None # The employee that the TimeCard is for
        self.breaks = [] # Holds all the Break objects related to this TimeCard instance

        self.hours_worked = 0 # Will hold the total number of hours for the timecard - factors in any breaks
        self.wages = 0.00

    @staticmethod
    def validate_time_card(data):
        is_valid = True

        if len(data["date"]) == 0:
            flash("Date must be present.", "timecard")

        # Test whether the input timecard data overlaps with an existing timecard
        all_timecards_for_date_employee = TimeCard.get_timecards_by_date(data)
        for this_timecard in all_timecards_for_date_employee:
            if this_timecard.time_in > data["time_in"] and this_timecard.time_in < data["time_out"]:
                flash("Time in cannot overlap a time out of another timecard.", "timecard")
                is_valid = False
                break
            if this_timecard.timeout < data["time_out"] and this_timecard.time_out > data["time_in"]:
                flash("Time out cannot overlap a time in of another timecard.", "timecard")
                is_valid = False
                break

        if len(data["time_in"]) == 0:
            flash("Time in must be present.", "timecard")
            is_valid = False
        if data["time_in"] >= data["time_out"]:
            flash("Time in must be less than time out.", "timecard")
            is_valid = False
        if len(data["time_out"]) == 0:
            flash("Time out must be present.", "timecard")

        return is_valid

    @staticmethod
    def validate_existing_time_card(data):
        is_valid = True

        if len(data["date"]) == 0:
            flash("Date must be present.", "timecard")

        # Test whether the input timecard data overlaps with a separate existing timecard
        all_timecards_for_date_employee = TimeCard.get_timecards_by_date_exclude(data)
        for this_timecard in all_timecards_for_date_employee:
            if this_timecard.time_in > data["time_in"] and this_timecard.time_in < data["time_out"]:
                flash("Time in cannot overlap a time out of another timecard.", "timecard")
                is_valid = False
                break
            if this_timecard.timeout < data["time_out"] and this_timecard.time_out > data["time_in"]:
                flash("Time out cannot overlap a time in of another timecard.", "timecard")
                is_valid = False
                break

        if len(data["time_in"]) == 0:
            flash("Time in must be present.", "timecard")
            is_valid = False
        if data["time_in"] >= data["time_out"]:
            flash("Time in must be less than time out.", "timecard")
            is_valid = False
        if len(data["time_out"]) == 0:
            flash("Time out must be present.", "timecard")

        return is_valid

    # Assume the times are in the format XX:XX (24-hour time format) and that time_two is greater than time_one
    @staticmethod
    def delta_time(time_one, time_two):
        if len(time_one) != 8:
            time_one = "0" + time_one
        if len(time_two) != 8:
            time_two = "0" + time_one

        time_one = time_one[:5]
        time_two = time_two[:5]
        
        time_one_hours = int(time_one[:2])
        time_one_minutes = int(time_one[3:])
        time_two_hours = int(time_two[:2])
        time_two_minutes = int(time_two[3:])

        delta_hours = time_two_hours - time_one_hours
        delta_minutes = time_two_minutes - time_one_minutes

        if delta_minutes < 0:
            delta_minutes = 60 + delta_minutes
            delta_hours -= 1

        return [delta_hours, delta_minutes]

    @staticmethod
    def calculate_hours_worked(the_timecard):
        #print(the_timecard.time_in)

        total_hours, total_minutes = TimeCard.delta_time(str(the_timecard.time_in), str(the_timecard.time_out))

        hours_worked = total_hours + round(total_minutes / 60, 2)

        return hours_worked

    @classmethod
    def create_time_card(cls, data):
        query = """
        INSERT INTO timecards
        (date, time_in, time_out, employee_id)
        VALUES (%(date)s, %(time_in)s, %(time_out)s, %(employee_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_time_cards(cls):
        query = """
        SELECT * FROM timecards
        JOIN employees ON employees.id = timecards.employee_id
        LEFT JOIN breaks ON breaks.timecard_id = timecards.id
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        all_timecards = []
        if len(results) > 0:
            for time_card_obj in results:
                pass

        return all_timecards

    @classmethod
    def get_all_time_cards_for_user(cls, data):
        query = """
        SELECT * FROM employees
        LEFT JOIN timecards ON employees.id = timecards.employee_id
        LEFT JOIN breaks ON breaks.timecard_id = timecards.id
        WHERE employees.id = %(employee_id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        employee_obj = None
        if len(results) > 0:
            employee_data = results[0]
            employee_obj = employee.Employee(employee_data)
            i = 0
            while i < len(results):
                if results[i]["timecards.id"] != None:
                    timecard_obj = cls({
                        "id": results[i]["timecards.id"],
                        "date": results[i]["date"],
                        "time_in": results[i]["time_in"],
                        "time_out": results[i]["time_out"],
                        "created_at": results[i]["timecards.created_at"],
                        "updated_at": results[i]["timecards.updated_at"]
                    })
                    timecard_obj.hours_worked = cls.calculate_hours_worked(timecard_obj)
                    employee_obj.timecards.append(timecard_obj)
                i += 1
        return employee_obj

    @classmethod
    def get_timecards_by_week(cls, data):
        query = """
        SELECT * FROM employees
        LEFT JOIN timecards ON employees.id = timecards.employee_id
        LEFT JOIN breaks ON breaks.timecard_id = timecards.id;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        all_employees = []
        if len(results) > 0:
            i = 0
            while i < len(results):
                current_employee = employee.Employee(results[i])
                if results[i]["timecards.id"] != None:
                    while i < len(results) and current_employee.id == results[i]["id"]:
                        timecard_obj = cls({
                            "id": results[i]["timecards.id"],
                            "date": results[i]["date"],
                            "time_in": results[i]["time_in"],
                            "time_out": results[i]["time_out"],
                            "created_at": results[i]["timecards.created_at"],
                            "updated_at": results[i]["timecards.updated_at"]
                        })
                        if timecard_obj.date >= data["week_start"] and timecard_obj.date <= data["week_end"]:
                            timecard_obj.hours_worked = cls.calculate_hours_worked(timecard_obj)
                            current_employee.timecards.append(timecard_obj)
                        i += 1
                else:
                    i += 1
                all_employees.append(current_employee)
        return all_employees

    @classmethod
    def get_timecards_by_date(cls, data):
        query = """
        SELECT * FROM timecards
        JOIN employees ON employees.id = timecards.employee_id
        LEFT JOIN breaks ON breaks.timecard_id = timecards.id
        WHERE employees.id = %(employee_id)s AND date = %(date)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        all_timecards = []
        if len(results) > 0:
            for this_timecard_data in all_timecards:
                this_timecard = cls(this_timecard_data)
                employee_obj = employee.Employee({
                    "id": results[0]["employees.id"],
                    "first_name": results[0]["first_name"],
                    "last_name": results[0]["last_name"],
                    "email": results[0]["email"],
                    "password": results[0]["password"],
                    "phone_number": results[0]["phone_number"],
                    "birthdate": results[0]["birthdate"],
                    "pay_rate": results[0]["pay_rate"],
                    "avatar_url": results[0]["avatar_url"],
                    "status": results[0]["status"],
                    "is_manager": results[0]["is_manager"],
                    "pin_code": results[0]["pin_code"],
                    "reg_code": results[0]["reg_code"],
                    "created_at": results[0]["employees.created_at"],
                    "updated_at": results[0]["employees.updated_at"]
                })
                this_timecard.employee = employee_obj
                this_timecard.hours_worked = cls.calculate_hours_worked(this_timecard)
                all_timecards.append(this_timecard)
        return all_timecards

    @classmethod
    def get_timecards_by_date_exclude(cls, data):
        query = """
        SELECT * FROM timecards
        JOIN employees ON employees.id = timecards.employee_id
        LEFT JOIN breaks ON breaks.timecard_id = timecards.id
        WHERE employees.id = %(employee_id)s AND date = %(date)s AND timecards.id != %(timecard_id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        all_timecards = []
        if len(results) > 0:
            for this_timecard_data in all_timecards:
                this_timecard = cls(this_timecard_data)
                employee_obj = employee.Employee({
                    "id": results[0]["employees.id"],
                    "first_name": results[0]["first_name"],
                    "last_name": results[0]["last_name"],
                    "email": results[0]["email"],
                    "password": results[0]["password"],
                    "phone_number": results[0]["phone_number"],
                    "birthdate": results[0]["birthdate"],
                    "pay_rate": results[0]["pay_rate"],
                    "avatar_url": results[0]["avatar_url"],
                    "status": results[0]["status"],
                    "is_manager": results[0]["is_manager"],
                    "pin_code": results[0]["pin_code"],
                    "reg_code": results[0]["reg_code"],
                    "created_at": results[0]["employees.created_at"],
                    "updated_at": results[0]["employees.updated_at"]
                })
                this_timecard.employee = employee_obj
                this_timecard.hours_worked = cls.calculate_hours_worked(this_timecard)
                all_timecards.append(this_timecard)
        return all_timecards

    @classmethod
    def get_timecard(cls, data):
        query = """
        SELECT * FROM timecards
        JOIN employees ON employees.id = timecards.employee_id
        LEFT JOIN breaks ON breaks.timecard_id = timecards.id
        WHERE timecards.id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        this_timecard = None
        if len(results) > 0:
            this_timecard = cls(results[0])
            employee_obj = employee.Employee({
                "id": results[0]["employees.id"],
                "first_name": results[0]["first_name"],
                "last_name": results[0]["last_name"],
                "email": results[0]["email"],
                "password": results[0]["password"],
                "phone_number": results[0]["phone_number"],
                "birthdate": results[0]["birthdate"],
                "pay_rate": results[0]["pay_rate"],
                "avatar_url": results[0]["avatar_url"],
                "status": results[0]["status"],
                "is_manager": results[0]["is_manager"],
                "pin_code": results[0]["pin_code"],
                "reg_code": results[0]["reg_code"],
                "created_at": results[0]["employees.created_at"],
                "updated_at": results[0]["employees.updated_at"]
            })
            this_timecard.employee = employee_obj
            this_timecard.hours_worked = cls.calculate_hours_worked(this_timecard)
        
        return this_timecard

    @classmethod
    def update_time_card(cls, data):
        query = """
        UPDATE timecards
        SET date = %(date)s,
        time_in = %(time_in)s,
        time_out = %(time_out)s
        WHERE id = %(timecard_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_time_card(cls, data):
        query = """
        DELETE FROM timecards WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)