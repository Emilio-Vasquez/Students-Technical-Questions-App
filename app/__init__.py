from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)
    
    app.secret_key = "MySecretKeyIsDog2025"  ## Not sure what to put just yet so I just put gibberish
    app.register_blueprint(main)
    
    return app
