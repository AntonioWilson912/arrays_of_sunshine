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
        all_timecards_for_date_employee = get_timecards_by_date(data)
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
        time_one_hours = int(time_one[:2])
        time_one_minutes = int(time_one[3:])
        time_two_hours = int(time_two[:2])
        time_two_minutes = int(time_two[3:])

        delta_hours = time_two_hours - time_one_hours
        delta_minutes = time_two_minutes - time_two_minutes

        if delta_minutes < 0:
            delta_minutes = 60 + delta_minutes
            delta_hours -= 1

        return [delta_hours, delta_minutes]

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
        SELECT * FROM timecards
        JOIN employees ON employees.id = timecards.employee_id
        LEFT JOIN breaks ON breaks.timecard_id = timecards.id
        WHERE employees.id = %(employee_id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        timecards = []
        if len(results) > 0:
            for timecard_dict in results:
                timecard_obj = cls(timecard_dict)
                employee_obj = employee.Employee({
                    "id": timecard_dict["employees.id"],
                    "first_name": timecard_dict["first_name"],
                    "last_name": timecard_dict["last_name"],
                    "email": timecard_dict["email"],
                    "password": timecard_dict["password"],
                    "phone_number": timecard_dict["phone_number"],
                    "birthdate": timecard_dict["birthdate"],
                    "pay_rate": timecard_dict["pay_rate"],
                    "avatar_url": timecard_dict["avatar_url"],
                    "status": timecard_dict["status"],
                    "is_manager": timecard_dict["is_manager"],
                    "pin_code": timecard_dict["pin_code"],
                    "reg_code": timecard_dict["reg_code"],
                    "created_at": timecard_dict["employees.created_at"],
                    "updated_at": timecard_dict["employees.updated_at"]
                })
                timecard_obj.employee = employee_obj

                timecards.append(timecard_obj)
        
        return timecards

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
                all_timecards.append(this_timecard)
        return all_timecards

    @classmethod
    def get_timecard(cls, data):
        query = """
        SELECT * FROM timecards
        JOIN employees ON employees.id = timecards.employee_id
        LEFT JOIN breaks ON breaks.timecard_id = timecards.id
        WHERE id = %(id)s;
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
        
        return this_timecard

    @classmethod
    def update_time_card(cls, data):
        query = """
        UPDATE timecards
        SET date = %(date)s,
        time_in = %(time_in)s,
        time_out = %(time_out)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_time_card(cls, data):
        query = """
        DELETE FROM timecards WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)