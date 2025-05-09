from app.extensions import os, request, jsonify, Blueprint, DeepFace
from app.utils.verify_image import verify_images
from app.models.face_reference import FaceReference
from app.function.face_verification_logic import verify_face_logic

recognition_bp = Blueprint('recognition', __name__)

@recognition_bp.route('/verify', methods=['POST'])
def verifyface():
    img_upload = request.files.get("image")
    user_id = request.form.get("user_id")

    if not img_upload or not user_id:
        return jsonify({"error": "image and user_id are required"}), 400

    result, status_code = verify_face_logic(user_id, img_upload)
    return jsonify(result), status_code
