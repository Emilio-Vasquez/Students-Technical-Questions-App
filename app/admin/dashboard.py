from flask import render_template
from app.admin.routes import admin_bp
from app.admin.utils import admin_required

@admin_bp.route('/')
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')