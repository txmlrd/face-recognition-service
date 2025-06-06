from app.extensions import os, request, jsonify, Blueprint, DeepFace, jwt_required, get_jwt_identity, redis_client
from app.models.face_reference import FaceReference
from app.function.face_verification_logic import verify_face_logic
from app.config import Config
import requests


admin_auth_bp = Blueprint('admin_auth_bp', __name__)
@admin_auth_bp.route('/inject-crucial-token', methods=['POST'])
@jwt_required()
def inject_crucial_token():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({
            "status": "failed",
            "message": "user_id is required",
            "data": None
        }), 400

    # Cek apakah user_id valid dengan request ke user service
    try:
        # Ganti URL ini sesuai alamat user-service kamu
        user_service_url = f"{Config.USER_SERVICE_URL}/admin/get-user?user_id={user_id}"
        headers = {"Authorization": request.headers.get("Authorization")}

        response = requests.get(user_service_url, headers=headers)

        if response.status_code != 200:
            return jsonify({
                "status": "failed",
                "message": f"user_id {user_id} not found in user service",
                "data": response.json()
            }), 404

    except Exception as e:
        return jsonify({
            "status": "failed",
            "message": "Failed to connect to user service",
            "data": str(e)
        }), 502

    # Jika user valid, inject ke Redis
    try:
        key = f"crucial_token:{user_id}"
        redis_client.setex(key, Config.CRUCIAL_ACCESS_TOKEN_EXPIRES, "true")

        return jsonify({
            "status": "success",
            "message": f"Crucial token injected successfully",
            "data": {
                "user_id": user_id,
                "key": key,
                "value": "true",
                "expires_in_seconds": Config.CRUCIAL_ACCESS_TOKEN_EXPIRES
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "failed",
            "message": "An error occurred while injecting crucial token",
            "data": str(e)
        }), 500


  
@admin_auth_bp.route('/delete-crucial-token', methods=['DELETE'])
def delete_crucial_token():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({
            "status": "failed",
            "message": "user_id is required",
            "data": None
        }), 400

    try:
        key = f"crucial_token:{user_id}"
        result = redis_client.delete(key)

        if result == 1:
            return jsonify({
                "status": "success",
                "message": f"Crucial token for deleted successfully",
                "data": {
                    "user_id": user_id,
                    "key": key
                }
            }), 200
        else:
            return jsonify({
                "status": "failed",
                "message": f"No crucial token found for user {user_id}",
                "data": {
                    "user_id": user_id,
                    "key": key
                }
            }), 404
    except Exception as e:
        return jsonify({
            "status": "failed",
            "message": "An error occurred while deleting crucial token",
            "data": str(e)
        }), 500

