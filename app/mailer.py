"""
mailer.py

Initializes the Flask-Mail extension to enable email functionality in the application.
The `mail` object can be imported and used wherever email sending is required.
"""
from flask_mail import Mail

mail = Mail()