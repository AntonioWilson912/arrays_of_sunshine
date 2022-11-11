from flask_app import app
from flask_app.models import employee, role

@app.route("/")
def index():
    return "App started!"