# ------------------------------
# System Tools
# ------------------------------
from flask import render_template
from app.admin.routes import admin_bp
from app.admin.utils import superadmin_required

@admin_bp.route('/reset_submissions')
@superadmin_required
def reset_submissions():
    return "Reset All Submissions"

@admin_bp.route('/export_data')
@superadmin_required
def export_data():
    return "Export Submissions (CSV)"