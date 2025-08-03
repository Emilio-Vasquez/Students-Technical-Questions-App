from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Routes are registered in submodules:
from app.admin import dashboard, questions, submissions, users, feedback, tools, test_cases
