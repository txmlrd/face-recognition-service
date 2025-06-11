from app import mail
from flask_mail import Message
from flask import current_app

def send_email(subject, recipient, html=None, body=None):
    msg = Message(subject, sender=current_app.config['MAIL_USERNAME'], recipients=[recipient])
    if html:
        msg.html = html
    if body:
        msg.body = body
    mail.send(msg)
