# ------------------------------
# Submissions
# ------------------------------
from flask import render_template
from app.admin.routes import admin_bp
from app.admin.utils import admin_required

@admin_bp.route('/view_submissions')
@admin_required
def view_submissions():
    return "View Submissions Page"

@admin_bp.route('/submission_stats')
@admin_required
def submission_stats():
    return "Submission Analytics Page"