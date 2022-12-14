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

        self.timecards = []
        self.role = None

    @staticmethod
    def validate_new_employee(data):
        is_valid = True

        if Employee.get_employee_by_email(data):
            flash("Email is already in use!", "new_employee")
            is_valid = False
        if len(data["first_name"]) < 3:
            flash("First name must be at least 3 characters.", "new_employee")
            is_valid = False
        if len(data["last_name"]) < 3:
            flash("Last name must be at least 3 characters.", "new_employee")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email format: someone@example.com", "new_employee")
        if len(data["phone_number"]) > 0 and not re.match(r'[\d]{3}-[\d]{3}-[\d]{4}', data["phone_number"]):
            flash("Invalid phone number format: 000-000-0000", "new_employee")
            is_valid = False
        if int(data["role_id"]) == -1:
            flash("Must choose a valid role.", "new_employee")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_register_employee(data):
        is_valid = True 
        # Assume true and assign false if it is not valid.

        employee_data = Employee.get_employee_by_email(data)

        if not employee_data:
            flash("Invalid email address!", "register")
            is_valid = False
        else:
            if employee_data.password:
                flash("Email has already been registered!", "register")
                return False
            
            if (data['reg_code']) != employee_data.reg_code:
                flash("Invalid registration code!", 'register')
                is_valid = False
            if data["password"] != data["confirm_password"]:
                flash("Passwords must match.", "register")
                is_valid = False
            if len(data["password"]) < 8:
                flash("Password must be at least 8 characters.", "register")
                is_valid = False
            if not re.findall("[\d]", data["password"]):
                flash("Password must contain at least 1 digit.", "register")
                is_valid = False
            if not re.findall("[^\w\s]", data["password"]):
                flash("Password must contain at least 1 special character.", "register")
                is_valid = False
        return is_valid

    @staticmethod
    def validate_login_employee(data):
        is_valid = True
        
        db_data = Employee.get_employee_by_email(data)
        
        if not db_data:
            flash("Invalid Email/Password", 'login')
            return False
        if not bcrypt.check_password_hash(db_data.password, data['password']):
            # if we get False after checking the password
            flash("Invalid Email/Password",'login')
            return False
        return is_valid

    @staticmethod
    def validate_reset_password(data):
        is_valid = True

        if not Employee.get_employee_by_email(data):
            flash("Email is not associated with an existing account.", "reset_password")
            is_valid = False
        else:
            if data["password"] != data["confirm_password"]:
                flash("Passwords must match.", "register")
                is_valid = False
            if len(data["password"]) < 8:
                flash("Password must be at least 8 characters.", "reset_password")
                is_valid = False
            if not re.findall("[\d]", data["password"]):
                flash("Password must contain at least 1 digit.", "reset_password")
                is_valid = False
            if not re.findall("[^\w\s]", data["password"]):
                flash("Password must contain at least 1 special character.", "reset_password")
                is_valid = False

        return is_valid

    @staticmethod
    def validate_update_employee(data):
        is_valid = True

        if len(data["first_name"]) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(data["last_name"]) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False

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
        WHERE email = %(email)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def reset_employee_password(cls, data):
        query = """
        UPDATE employees
        SET password = %(password)s
        WHERE email = %(email)s;
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
    def get_all_current_employees(cls):
        query = """
        SELECT * FROM employees
        LEFT JOIN roles ON employees.role_id = roles.id
        WHERE status = "HIRED";
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
    def get_all_terminated_employees(cls):
        query = """
        SELECT * FROM employees
        LEFT JOIN roles ON employees.role_id = roles.id
        WHERE status = "TERMINATED";
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
        SELECT * FROM employees
        LEFT JOIN roles ON employees.role_id = roles.id
        WHERE email = %(email)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        
        if len(results) == 0:
            return None
        employee_data = results[0]
        employee_obj = cls(employee_data)
        role_data = {
                    "id": employee_data["roles.id"],
                    "name": employee_data["name"],
                    "created_at": employee_data["roles.created_at"],
                    "updated_at": employee_data["roles.updated_at"]
                }
        role_obj = role.Role(role_data)
        employee_obj.role = role_obj
                
        return employee_obj
    
    @classmethod
    def get_employee_by_id(cls, data):
        query = """
        SELECT * FROM employees
        LEFT JOIN roles ON employees.role_id = roles.id
        WHERE employees.id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        
        employee_data = results[0]
        employee_obj = cls(employee_data)
        role_data = {
            "id": employee_data["roles.id"],
            "name": employee_data["name"],
            "created_at": employee_data["roles.created_at"],
            "updated_at": employee_data["roles.updated_at"]
        }
        role_obj = role.Role(role_data)
        employee_obj.role = role_obj
                
        return employee_obj

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
        
        return terminated_employees

    @classmethod
    def update_employee(cls, data):
        query = """
        UPDATE employees SET
        first_name = %(first_name)s,
        last_name = %(last_name)s,
        email = %(email)s,
        password = %(password)s,
        phone_number = %(phone_number)s,
        birthdate = %(birthdate)s,
        pay_rate = %(pay_rate)s,
        avatar_url = %(avatar_url)s,
        status = %(status)s,
        is_manager = %(is_manager)s,
        pin_code = %(pin_code)s,
        reg_code = %(reg_code)s,
        role_id = %(role_id)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def rehire_employee(cls, data):
        query = """
        UPDATE employees
        SET status = "HIRED"
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def terminate_employee(cls, data):
        query = """
        UPDATE employees
        SET status = "TERMINATED"
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_employee(cls, data):
        query = "DELETE FROM employees WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)