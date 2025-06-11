from PIL import Image
from io import BytesIO
import os
from flask_mail import Mail
from deepface import DeepFace
from flask import Flask, request, jsonify, Blueprint
import base64
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, create_refresh_token
from flask_migrate import Migrate
import redis
from app.config import Config

redis_client = redis.StrictRedis.from_url(Config.REDIS_URL)

DeepFace = DeepFace
mail = Mail()
jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()
os = os
BytesIO = BytesIO
Image = Image
Flask = Flask
request = request
jsonify = jsonify
base64 = base64
Blueprint = Blueprint
migrate = Migrate()
create_access_token = create_access_token
get_jwt_identity = get_jwt_identity
jwt_required = jwt_required
create_refresh_token = create_refresh_token