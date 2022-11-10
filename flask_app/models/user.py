from flask_app.config.mysqlconnection import connectToMySQL

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.phone_number = data["phone_number"]
        self.birthdate = data["birthdate"]
        self.pay_rate = data["pay_rate"]
        self.avatar_url = data["avatar_url"]
        self.status = data["status"]
        self.is_manager = data["is_manager"]
        self.pin_code = data["pin_code"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.time_cards = []
        self.role = None

    @staticmethod
    def validate_register_user(data):
        pass

    @staticmethod
    def validate_login_user(data):
        pass

    @classmethod
    def create_user(cls, data):
        pass

    @classmethod
    def get_all_users(cls):
        pass

    @classmethod
    def get_all_terminated_users(cls):
        pass

    @classmethod
    def update_user(cls, data):
        pass

    @classmethod
    def delete_user(cls, data):
        pass