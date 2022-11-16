from flask_app import app
from flask_app.controllers import employees, timecards # INSERT OTHER CONTROLLERS HERE!

if __name__ == "__main__":
    app.run(debug=True)