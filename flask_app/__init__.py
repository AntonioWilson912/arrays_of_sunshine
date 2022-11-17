from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# For formatting dates in HTML
@app.template_filter("strftime")
def _jinja2_filter_datetime(value, format="%B %d, %Y"):
    return value.strftime(format)