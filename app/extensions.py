from PIL import Image
from io import BytesIO
import os
from deepface import DeepFace
from flask import Flask, request, jsonify, Blueprint
import base64
from flask_sqlalchemy import SQLAlchemy

DeepFace = DeepFace
db = SQLAlchemy()
os = os
BytesIO = BytesIO
Image = Image
Flask = Flask
request = request
jsonify = jsonify
base64 = base64
Blueprint = Blueprint