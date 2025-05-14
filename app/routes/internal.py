from flask import Blueprint, request, jsonify


# internal_bp = Blueprint('internal', __name__)
# @internal_bp.route('/delete-face', methods=['POST'])
# def delete_face():
#     data = request.form
#     user_id = data.get('user_id')
#     face_model = data.get('face_model')

#     if not user_id or not face_model:
#         return jsonify({"error": "User ID and face model are required"}), 400

#     # Call the recognition service to delete the face
#     recognition_service_url = f"{Config.RECOGNITION_SERVICE_URL}/delete-face"
#     response = requests.post(recognition_service_url, data={"user_id": user_id, "face_model": face_model})

#     if response.status_code != 200:
#         return jsonify({"error": "Failed to delete face"}), 500

#     return jsonify({"message": "Face deleted successfully"}), 200