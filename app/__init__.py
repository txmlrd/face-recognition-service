from app.extensions import  Flask, db, migrate, bcrypt, jwt
from app.routes.recognition import recognition_bp
from app.routes.auth import auth_bp
from app.config import Config
from app.models.face_reference import FaceReference

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # jwt(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Membuat tabel jika belum ada
    with app.app_context():
        db.create_all()  # Ini akan membuat tabel berdasarkan model yang ada
    
    app.register_blueprint(recognition_bp)
    app.register_blueprint(auth_bp)
    
    @app.route('/')
    def index():
        return "Welcome to the Face Recognition API!"
    
    return app
