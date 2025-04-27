from extensions import DeepFace, os, BytesIO, Image, Flask, request, jsonify
from routes.recognition import recognition_bp

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(recognition_bp)
    return app



