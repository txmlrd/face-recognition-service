from PIL import Image
from io import BytesIO
import os
from deepface import DeepFace
from flask import Flask, request, jsonify, Blueprint
import base64

DeepFace = DeepFace
os = os
BytesIO = BytesIO
Image = Image
Flask = Flask
request = request
jsonify = jsonify
base64 = base64
Blueprint = Blueprint