from app import db
from datetime import datetime

class PasswordReset(db.Model):
    __tablename__ = 'password_resets'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_reset = db.Column(db.Boolean, default=False)
