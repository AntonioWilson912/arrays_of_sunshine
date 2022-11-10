from flask_app.config.mysqlconnection import connectToMySQL

class Role:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all_roles(cls):
        pass

    @classmethod
    def get_role(cls, data):
        pass