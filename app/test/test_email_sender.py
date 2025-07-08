import unittest
from flask import Flask
from flask_mail import Mail, Message
from config import Config

class TestEmailSender(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)

        self.mail = Mail(self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_send_email(self):
        with self.mail.connect() as conn:
            msg = Message(
                subject="Test Email from Technical Questions App",
                sender=self.app.config['MAIL_DEFAULT_SENDER'],
                recipients=["emiliovasquezcarbajalalexander@gmail.com"],  # Replace with your test email
                body="This is a test email to verify SMTP configuration."
            )
            response = conn.send(msg)
            self.assertIsNone(response)  # If no exception is raised, the test passes

if __name__ == "__main__":
    unittest.main()

## RUn this code on the root directory to test: python -m unittest app/test/test_email_sender.py
