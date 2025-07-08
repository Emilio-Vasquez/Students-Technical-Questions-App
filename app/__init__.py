from flask import Flask
from .routes import main
from config import Config
from markdown import markdown
from .mailer import mail
from .forgot_password import forgot_password_bp
from .reset_password import reset_password_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(main)
    app.register_blueprint(forgot_password_bp)
    app.register_blueprint(reset_password_bp)

    mail.init_app(app)
    
    @app.template_filter('markdown')
    def markdown_filter(text):
        return markdown(text)
    
    @app.template_filter('format_language')
    def format_language(lang):
        if lang.lower() == "sql":
            return "SQL"
        return lang.capitalize()
    
    return app