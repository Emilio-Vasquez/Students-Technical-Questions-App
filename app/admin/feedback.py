# ------------------------------
# Feedback
# ------------------------------
from flask import render_template
from app.admin.routes import admin_bp
from app.admin.utils import admin_required

@admin_bp.route('/feedback_inbox')
@admin_required
def feedback_inbox():
    return "Feedback Inbox"