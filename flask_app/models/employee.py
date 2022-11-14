from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import role
from flask import flash

from flask_bcrypt import Bcrypt
from flask_app import app
import re
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

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
        is_valid = True 
        # Assume true and assign false if it is not valid.
        if not Employee.get_employee_by_email(data):
            return False
        
        db_data = Employee.get_employee_by_email(data)
        
        if (data['email']) != db_data['email']:
                flash(u"Invalid email address!", 'email_invalid')
                is_valid = False
        
        if (data['reg_code']) != db_data['reg_code']:
                flash(u"Registration Code Invalid!.", 'confirm_password')
                is_valid = False
        return is_valid

    @staticmethod
    def validate_login_employee(data):
        is_valid = True
        
        if not Employee.get_employee_by_email(data):
            return False
        
        db_data = Employee.get_employee_by_email(data)
        
        if not data:
            flash(u"Invalid Email/Password", 'invalid_email_or_password')
            return False
        if not bcrypt.check_password_hash(data['password'], db_data['password'] ):
            # if we get False after checking the password
            flash(u"Invalid Email/Password",'invalid_password')
            return False
        return is_valid

    @classmethod
    def create_employee(cls, data):
        query = """
        INSERT INTO employees
        (first_name, last_name, email, phone_number, pin_code, reg_code, role_id)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone_number)s, %(pin_code)s, %(reg_code)s, %(role_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def register_employee(cls, data):
        query = """
        UPDATE employees
        SET password = %(password)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_employees(cls):
        query = """
        SELECT * FROM employees
        LEFT JOIN roles ON employees.role_id = roles.id;
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

                employees.append(employee)

        return employees
    
    @classmethod
    def get_employee_by_email(cls, data):
        query = """
        SELECT * From employees WHERE email = %(email)s
        LEFT JOIN roles ON employees.role_id = roles.id;
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        
        employee_data = cls(results[0])
        role_data = {
                    "id": employee_data["roles.id"],
                    "name": employee_data["name"],
                    "created_at": employee_data["roles.created_at"],
                    "updated_at": employee_data["roles.updated_at"]
                }
        role_obj = role.Role(role_data)
        employee_data.role = role_obj
                
        return employee_data
        
        
        

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