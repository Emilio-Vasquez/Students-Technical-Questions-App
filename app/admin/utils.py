from flask import session, redirect, url_for, flash
from functools import wraps

def admin_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if session.get('role') not in ['moderator', 'superadmin']:
            flash("Admin access required.", "danger")
            return redirect(url_for('main.home'))
        return view_function(*args, **kwargs)
    return wrapper

def superadmin_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if session.get('role') != 'superadmin':
            flash("Superadmin access required.", "danger")
            return redirect(url_for('main.home'))
        return view_function(*args, **kwargs)
    return wrapper

def moderator_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if session.get('role') not in ['moderator', 'superadmin']:
            flash("Moderator access required.", "danger")
            return redirect(url_for('main.home'))
        return view_function(*args, **kwargs)
    return wrapper
