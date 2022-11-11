from flask_app.config.mysqlconnection import connectToMySQL

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
        pass

    @classmethod
    def get_all_breaks_for_time_card(cls, data):
        pass

    @classmethod
    def update_break_for_time_card(cls, data):
        pass

    @classmethod
    def delete_break_from_time_card(cls, data):
        pass