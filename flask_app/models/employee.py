from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import role

class Employee:

    db_name = "arrays_of_sunshine"

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
        self.pin_code = data["pin_code"] # Code used for clocking into a shift (future feature)
        self.reg_code = data["reg_code"] # Code used to register an account
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.time_cards = []
        self.role = None

    @staticmethod
    def validate_register_employee(data):
        pass

    @staticmethod
    def validate_login_employee(data):
        pass

    @classmethod
    def create_employee(cls, data):
        pass

    @classmethod
    def get_all_employees(cls):
        query = """
        SELECT * FROM employees
        JOIN roles ON employees.role_id = roles.id;
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        employees = []
        if len(results) > 0:
            for employee_data in results:
                employee = cls(employee_data)
                role_data = {
                    "id": employee_data["roles.id"],
                    "name": employee_data["name"],
                    "created_at": employee_data["roles.created_at"],
                    "updated_at": employee_data["roles.updated_at"]
                }
                role_obj = role.Role(role_data)
                employee.role = role_obj

        return employees

    @classmethod
    def get_all_reg_codes(cls):
        pass

    @classmethod
    def get_all_terminated_employees(cls):
        query = """
        SELECT * FROM employees
        JOIN roles ON employees.role_id = roles.id
        WHERE status = "TERMINATED";
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        terminated_employees = []
        if len(results) > 0:
            for terminated_employee in results:
                employee = cls(terminated_employee)
                role_data = {
                    "id": terminated_employee["roles.id"],
                    "name": terminated_employee["name"],
                    "created_at": terminated_employee["roles.created_at"],
                    "updated_at": terminated_employee["roles.updated_at"]
                }
                role_obj = role.Role(role_data)
                employee.role = role_obj
        
        return terminated_employee

    @classmethod
    def update_employee(cls, data):
        pass

    @classmethod
    def delete_employee(cls, data):
        query = "DELETE FROM employees WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)