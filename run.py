"""
This is the entry point for the Technical Questions App Flask application.

This script initializes and runs the Flask app instance using the
application factory pattern defined in app/__init__.py.

Usage:
    python run.py - At root directory

The app is configured to run in debug mode on all available IPs (0.0.0.0) at port 5000.
Still in the process of development.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)