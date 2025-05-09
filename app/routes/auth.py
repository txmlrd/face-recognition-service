import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.models.face_reference import FaceReference
from datetime import datetime
from app.extensions import db, create_access_token, get_jwt_identity, jwt_required
from app.function.face_verification_logic import verify_face_logic
from extensions import bcrypt
import requests


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/upload-face', methods=['POST'])
@jwt_required()
def upload_faces():
    user_id = request.form.get('user_id')
    images = request.files.getlist('images')  # Ambil semua file dengan key 'images'

    if not user_id or len(images) != 3:
        return jsonify({'message': 'user_id dan 3 image files wajib dikirim'}), 400

    try:
        save_path = os.path.join("storage", "faces", str(user_id))
        
        new_face_references = FaceReference(user_id=user_id, image_path=save_path, created_at=datetime.utcnow())
        # Simpan ke database
        db.session.add(new_face_references)
        db.session.commit()
        os.makedirs(save_path, exist_ok=True)

        for i, image in enumerate(images, start=1):
            filename = secure_filename(f"img_{i}.jpg")
            image.save(os.path.join(save_path, filename))

        return jsonify({'message': 'Semua gambar berhasil diupload'}), 200
    except Exception as e:
        return jsonify({'message': 'Upload gagal', 'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.form
    email, password = data.get('email'), data.get('password')

    user_service_url = f"http://user-service:5001/internal/user-by-email?email={email}"  # sesuaikan URL dan port
    user_response = requests.get(user_service_url)
    
    if user_response.status_code != 200:
        return jsonify({"error": "User not found"}), 404
    
    user = user_response.json()
    password_user = user.get('password')
    is_verified = user.get('is_verified')
    user_id = user.get('id')

    if user and bcrypt.check_password_hash(password_user, password):
        if not is_verified:
            return jsonify({"error": "Email not verified"}), 401
        access_token = create_access_token(identity=str(user_id))
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Invalid credentials"}), 401
    
    
# Logout
@auth_bp.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    try :
        user = get_jwt_identity()
        return jsonify({"user_id": user}), 200
    except Exception as e:
        return jsonify({"msg": "Token is invalid"}), 401
    

@auth_bp.route('/login-face', methods=['POST'])
def login_face():
    data = request.form
    email = data.get('email')
    face = request.files.get('face_image')
    
    if not email or not face:
        return jsonify({"error": "Email and face image are required"}), 400

    # Cari user berdasarkan username atau email
    user_service_url = f"http://user-service:5001/internal/user-by-email?email={email}"  # sesuaikan URL dan port
    user_response = requests.get(user_service_url)

    user = user_response.json()
    if user_response.status_code != 200:
        return jsonify({"error": "User not found"}), 404
    user_id = user['id']
    
    result, status_code = verify_face_logic(user_id, face)

    if result.get('match'):
        return jsonify(access_token=create_access_token(identity=str(user_id))), 200
    return jsonify({"error": "Face recognition failed", "details": result}), status_code


