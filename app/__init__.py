from extensions import DeepFace, os, BytesIO, Image, Flask, request, jsonify, db
from routes.recognition import recognition_bp
from routes.auth import auth_bp
from config import Config
from models.face_reference import FaceReference  # Pastikan model di-import

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # jwt(app)
    db.init_app(app)
    
    # Membuat tabel jika belum ada
    with app.app_context():
        db.create_all()  # Ini akan membuat tabel berdasarkan model yang ada
    
    app.register_blueprint(recognition_bp)
    app.register_blueprint(auth_bp)
    
    @app.route('/')
    def index():
        return "Welcome to the Face Recognition API!"
    
    return app
