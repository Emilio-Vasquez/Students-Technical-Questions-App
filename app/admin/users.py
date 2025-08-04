
# ------------------------------
# User Management
# ------------------------------
from flask import render_template, session
from app.admin.routes import admin_bp
from app.admin.utils import superadmin_required
from flask import request, redirect, url_for, flash
from app.db import get_db_connection

@admin_bp.route('/user_list')
@superadmin_required
def user_list():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id, username, email, role, created_at, is_verified FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('admin/user_list.html', users=users)

@admin_bp.route('/promote_user', methods=['POST'])
@superadmin_required
def promote_user():
    username = request.form.get('username')
    action = request.form.get('action')  # 'promote' or 'demote'

    if not username or action not in ['promote', 'demote']:
        flash('Invalid promotion request.', 'error')
        return redirect(url_for('admin.user_list'))

    if username == session.get('username'):
        flash("You cannot change your own role.", 'warning')
        return redirect(url_for('admin.user_list'))

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT id, role FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            flash("User not found.", 'error')
            return redirect(url_for('admin.user_list'))

        new_role = 'moderator' if action == 'promote' else 'user'
        cursor.execute("UPDATE users SET role = %s WHERE username = %s", (new_role, username))
        db.commit()

        flash(f"{username} has been {'promoted to Moderator' if action == 'promote' else 'demoted to User'}.", 'success')
    except Exception as e:
        db.rollback()
        flash(f"Error processing request: {str(e)}", 'error')
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('admin.user_list'))

@admin_bp.route('/verify_user', methods=['POST'])
@superadmin_required
def verify_user():
    username = request.form.get('username')
    action = request.form.get('action')  # 'verify' or 'unverify'

    if not username or action not in ['verify', 'unverify']:
        flash('Invalid verification request.', 'error')
        return redirect(url_for('admin.user_list'))

    db = get_db_connection()
    cursor = db.cursor()

    try:
        verify_status = 1 if action == 'verify' else 0
        cursor.execute("UPDATE users SET is_verified = %s WHERE username = %s", (verify_status, username))
        db.commit()
        flash(f"{username} has been {'verified' if action == 'verify' else 'unverified'}.", 'success')
    except Exception as e:
        db.rollback()
        flash(f"Error verifying user: {str(e)}", 'error')
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('admin.user_list'))

@admin_bp.route('/delete_users', methods=['POST'])
@superadmin_required
def delete_users():
    user_ids = request.form.getlist('user_ids')

    if not user_ids:
        flash("No users selected for deletion.", 'warning')
        return redirect(url_for('admin.user_list'))

    db = get_db_connection()
    cursor = db.cursor()

    try:
        format_strings = ','.join(['%s'] * len(user_ids))
        cursor.execute(f"DELETE FROM users WHERE id IN ({format_strings})", tuple(user_ids))
        db.commit()
        flash(f"{len(user_ids)} user(s) deleted successfully.", 'success')
    except Exception as e:
        db.rollback()
        flash(f"Error deleting users: {str(e)}", 'error')
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('admin.user_list'))