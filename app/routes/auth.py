import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
# from models.user import User
from extensions import bcrypt


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/upload-face', methods=['POST'])
def upload_faces():
    user_id = request.form.get('user_id')
    images = request.files.getlist('images')  # Ambil semua file dengan key 'images'

    if not user_id or len(images) != 3:
        return jsonify({'message': 'user_id dan 3 image files wajib dikirim'}), 400

    try:
        save_path = os.path.join("storage", "faces", str(user_id))
        os.makedirs(save_path, exist_ok=True)

        for i, image in enumerate(images, start=1):
            filename = secure_filename(f"img_{i}.jpg")
            image.save(os.path.join(save_path, filename))

        return jsonify({'message': 'Semua gambar berhasil diupload'}), 200
    except Exception as e:
        return jsonify({'message': 'Upload gagal', 'error': str(e)}), 500
    
# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.form
#     email, password = data.get('email'), data.get('password')

#     user = User.query.filter_by(email=email).first()

#     if user and bcrypt.check_password_hash(user.password, password):
#         if not user.is_verified:
#             return "Please verify your email before logging in.", 401
#         access_token = create_access_token(identity=username)
#         refresh_token = create_refresh_token(identity=username)
#     return "Invalid credentials", 401
    
    



