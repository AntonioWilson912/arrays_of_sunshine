from flask_app.config.mysqlconnection import connectToMySQL

class TimeCard:
    def __init__(self, data):
        self.id = data["id"]
        self.date = data["date"]
        self.time_in = data["time_in"]
        self.time_out = data["time_out"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.employee = None # The employee that the TimeCard is for
        self.breaks = [] # Holds all the Break objects related to this TimeCard instance

    @staticmethod
    def validate_time_card(data):
        pass

    @classmethod
    def create_time_card(cls, data):
        pass

    @classmethod
    def get_all_time_cards(cls, data):
        pass

    @classmethod
    def get_all_time_cards_for_user(cls, data):
        pass

    @classmethod
    def update_time_card(cls, data):
        pass

    @classmethod
    def delete_time_card(cls, data):
        pass