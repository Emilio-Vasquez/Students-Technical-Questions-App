
# ------------------------------
# User Management
# ------------------------------
from flask import render_template
from app.admin.routes import admin_bp
from app.admin.utils import superadmin_required

@admin_bp.route('/user_list')
@superadmin_required
def user_list():
    return "User List Page"

@admin_bp.route('/promote_user')
@superadmin_required
def promote_user():
    return "Promote/Demote User Page"

@admin_bp.route('/verify_user')
@superadmin_required
def verify_user():
    return "Verify/Unverify User Page"

@admin_bp.route('/delete_users')
@superadmin_required
def delete_users():
    return "Delete Users Page"
