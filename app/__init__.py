from app.extensions import  Flask, db, migrate, bcrypt, jwt, mail
from app.routes.recognition import recognition_bp
from app.routes.auth import auth_bp
from app.routes.admin.admin import admin_auth_bp
from app.config import Config
from app.models.face_reference import FaceReference
from app.models.password_reset import PasswordReset

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    
    app.register_blueprint(recognition_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_auth_bp)
    
    @app.route('/')
    def index():
        return "Welcome to the Auth And Security Service!"
    
    return app
