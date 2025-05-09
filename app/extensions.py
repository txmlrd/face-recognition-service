from PIL import Image
from io import BytesIO
import os
from deepface import DeepFace
from flask import Flask, request, jsonify, Blueprint
import base64
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_migrate import Migrate

DeepFace = DeepFace
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