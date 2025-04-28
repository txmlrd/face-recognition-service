from extensions import DeepFace, os, BytesIO, Image, Flask, request, jsonify, db
from routes.recognition import recognition_bp
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(recognition_bp)
    
    @app.route('/')
    def index():
        return "Welcome to the Face Recognition API!"
    
    return app



