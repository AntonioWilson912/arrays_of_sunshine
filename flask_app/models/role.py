from flask_app.config.mysqlconnection import connectToMySQL

class Role:

    db_name = "arrays_of_sunshine"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all_roles(cls):
        query = "SELECT * FROM roles";
        results = connectToMySQL(cls.db_name).query_db(query)
        roles = []
        if len(results) > 0:
            for role in results:
                roles.append(cls(role))

        return roles

    @classmethod
    def get_role(cls, data):
        query = "SELECT * FROM roles WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0]) if len(results) > 0 else None