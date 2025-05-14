from app import db
from datetime import datetime

class FaceReference(db.Model):
    __tablename__ = 'face_references'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), nullable=False) 
    image_path = db.Column(db.String(255), nullable=False)  # simpan path ke file, bukan isi file
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
