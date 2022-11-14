from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import timecard

class Break:
    db_name = "arrays_of_sunshine"

    def __init__(self, data):
        self.id = data["id"]
        self.break_start = data["break_start"]
        self.break_finish = data["break_finish"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
        self.time_card = None # The time card that will be linked to this Break

    @staticmethod
    def validate_break(data):
        pass

    @classmethod
    def create_break(cls, data):
        query = """
        INSERT INTO breaks
        (break_start, break_finish, timecard_id)
        VALUES (%(break_start)s, %(break_finish)s, %(timecard_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_breaks_for_time_card(cls, data):
        query = """
        SELECT * FROM breaks
        JOIN timecards ON timecards.id = breaks.timecard_id
        WHERE timecards.id = %(timecard_id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        all_breaks = []
        if len(results) > 0:
            for break_dict in results:
                break_obj = cls(break_dict)
                timecard_obj = timecard.TimeCard({
                    "id": break_dict["timecards.id"],
                    "date": break_dict["date"],
                    "time_in": break_dict["time_in"],
                    "time_out": break_dict["time_out"],
                    "created_at": break_dict["timecards.created_at"],
                    "updated_at": break_dict["timecards.updated_at"]
                })
                break_obj.time_card = timecard_obj
                all_breaks.append(break_obj)

        return all_breaks


    @classmethod
    def update_break_for_time_card(cls, data):
        query = """
        UPDATE breaks
        SET break_start = %(break_start)s,
        break_finish = %(break_finish)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_break_from_time_card(cls, data):
        query = """
        DELETE FROM breaks WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)