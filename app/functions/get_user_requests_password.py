from app.models.password_reset import PasswordReset
from datetime import datetime
from sqlalchemy import desc

def get_user_request_password(uuid: str):
    if not uuid:
        return None, 400

    now = datetime.utcnow()
    token = (
        PasswordReset.query
        .filter_by(uuid=uuid, is_reset=False)
        .filter(PasswordReset.expires_at > now)
        .order_by(desc(PasswordReset.created_at)) 
        .first()
    )
    
    if token:
        return token, 200
    return None, 404