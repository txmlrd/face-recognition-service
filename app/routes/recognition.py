from app.extensions import os, request, jsonify, Blueprint, DeepFace, jwt_required, get_jwt_identity, redis_client
from app.models.face_reference import FaceReference
from app.function.face_verification_logic import verify_face_logic
from app.config import Config
import requests


recognition_bp = Blueprint('recognition', __name__)

@recognition_bp.route('/verify', methods=['POST'])
def verifyface():
    img_upload = request.files.get("image")
    user_id = request.form.get("user_id")

    if not img_upload or not user_id:
        return jsonify({"error": "image and user_id are required"}), 400

    result, status_code = verify_face_logic(user_id, img_upload)
    return jsonify(result), status_code

@recognition_bp.route('/crucial-verify', methods=['POST'])
@jwt_required()
def crucial_verify():
    data = request.form
    img_upload = request.files.get("image")
    selected_face_model = data.get('face_model_preference')
    user_id_token = get_jwt_identity()

    if not img_upload:
        return jsonify({"error": "Image is required"}), 400

    # Ambil data user dari user-service (butuh model preferensi sekarang)
    user_service_url = f"{Config.USER_SERVICE_URL}/internal/user-by-id?id={user_id_token}"
    user_response = requests.get(user_service_url)

    if user_response.status_code != 200:
        return jsonify({"error": "User not found"}), 404

    user = user_response.json()
    user_model_preference = user.get("face_model_preference")
    uuid = user['uuid']

    # Jalankan verifikasi wajah dengan model yang dipilih user
    result, status_code = verify_face_logic(uuid, img_upload, selected_face_model)

    if result.get("match"):
        # Update face model jika berbeda
        if selected_face_model and selected_face_model != user_model_preference:
            update_model_url = f"{Config.USER_SERVICE_URL}/update/face-model-preference"
            update_model_response = requests.post(
                update_model_url,
                data={"user_id": user_id_token, "face_model_preference": selected_face_model},
                headers={"Authorization": f"{request.headers.get('Authorization')}"}
            )

            if update_model_response.status_code != 200:
                return jsonify({"error": "Failed to update face model preference"}), 500

        # Set Redis token berlaku 15 menit
        redis_client.setex(f"crucial_token:{user_id_token}", Config.CRUCIAL_ACCESS_TOKEN_EXPIRES, "true")
        return jsonify({"message": "Crucial access granted for 15 minutes"}), 200

    return jsonify({"error": "Face verification failed"}), 400

    