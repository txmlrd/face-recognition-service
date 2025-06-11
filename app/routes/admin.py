from app.extensions import os, request, jsonify, Blueprint, DeepFace, jwt_required, get_jwt_identity, redis_client
from app.models.face_reference import FaceReference
from app.models.password_reset import PasswordReset
from app.function.face_verification_logic import verify_face_logic
from app.config import Config
import requests

admin_auth_bp = Blueprint('admin_auth_bp', __name__)

from datetime import datetime

@admin_auth_bp.route('/log-password', methods=['GET'])
@jwt_required()
def get_log_password():
    uuid = request.args.get('uuid')
    is_reset_str = request.args.get('is_reset')

    try:
        query = PasswordReset.query

        if uuid:
            query = query.filter_by(uuid=uuid)

        if is_reset_str is not None:
            is_reset = is_reset_str.lower() == 'true'
            query = query.filter_by(is_reset=is_reset)

        logs = query.all()
        now = datetime.utcnow()

        log_list = [{
            "id": log.id,
            "uuid": log.uuid,
            "token": log.token,
            "is_reset": log.is_reset,
            "created_at": log.created_at.isoformat(),
            "expires_at": log.expires_at.isoformat(),
            "is_expired": log.expires_at < now
        } for log in logs]

        return jsonify({
            "status": "success",
            "message": "Password reset logs retrieved successfully" if log_list else "No password reset logs found with the specified filter",
            "data": log_list
        }), 200

    except Exception as e:
        return jsonify({
            "status": "failed",
            "message": "An error occurred while retrieving password reset log(s)",
            "data": str(e)
        }), 500



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

    try:
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

