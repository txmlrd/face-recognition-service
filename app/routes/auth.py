import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.models.face_reference import FaceReference
from datetime import datetime
from app.extensions import db, create_access_token, get_jwt_identity, jwt_required, bcrypt, create_refresh_token
from app.function.face_verification_logic import verify_face_logic
import requests
from app.config import Config
from datetime import timedelta


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user_id = get_jwt_identity() 
        user_id = current_user_id
        user_service_url = f"{Config.USER_SERVICE_URL}/internal/user-by-id?id={user_id}"
        user_response = requests.get(user_service_url)

        if user_response.status_code != 200:
            return jsonify({"error": "User not found"}), 404
        
        
        role_id = user_response.json().get('role_id')
        uuid = user_response.json().get('uuid')
        
        role_service_url = f"{Config.ROLE_SERVICE_URL}/internal/role-name-by-role-id?role_id={role_id}"
        role_response = requests.get(role_service_url)
        
        if role_response.status_code != 200:
            return jsonify({"error": "Failed to fetch permissions"}), 500

        role_name = role_response.json().get("role_name")

        additional_claims = {
        "role_name": role_name,
        "uuid": uuid,
        "role_id": role_id,
        }
        new_access_token = create_access_token(
            identity=current_user_id,
            additional_claims=additional_claims
        )
        return jsonify(access_token=new_access_token), 200
    except Exception as e:
        return jsonify({"error": "Failed to refresh token", "details": str(e)}), 500
    
@auth_bp.route('/upload-face', methods=['POST'])
def upload_faces():
    uuid = request.form.get('uuid')
    images = request.files.getlist('images')

    if not uuid or len(images) != 3:
        return jsonify({
            'status': 'error',
            'message': 'UUID dan 3 file gambar wajib dikirim',
            'data': None
        }), 400

    try:
        # Cek apakah sudah ada entry face reference untuk uuid ini
        existing_ref = FaceReference.query.filter_by(uuid=uuid).first()

        if existing_ref:
            save_path = existing_ref.image_path
            # Hapus file lama di folder
            if os.path.exists(save_path):
                import shutil
                shutil.rmtree(save_path)
            # Buat folder baru (kosong)
            os.makedirs(save_path, exist_ok=True)
        else:
            # Jika belum ada, buat folder dan buat entry DB baru
            save_path = os.path.join("storage", "faces", str(uuid))
            os.makedirs(save_path, exist_ok=True)
            new_face_ref = FaceReference(uuid=uuid, image_path=save_path, created_at=datetime.utcnow())
            db.session.add(new_face_ref)
            db.session.commit()

        # Simpan gambar ke folder
        saved_files = []
        for i, image in enumerate(images, start=1):
            filename = secure_filename(f"img_{i}.jpg")
            image.save(os.path.join(save_path, filename))
            saved_files.append(filename)

        return jsonify({
            'status': 'success',
            'message': 'Face reference berhasil diupdate',
            'data': {
                'uuid': uuid,
                'saved_images': saved_files,
                'path': save_path
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Gagal upload face reference',
            'error': str(e),
            'data': None
        }), 500


@auth_bp.route('/check-face-reference/<uuid>', methods=['GET'])
def check_face_reference(uuid):
    try:
        folder_path = os.path.join("storage", "faces", str(uuid))
        
        # Cek apakah folder ada
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return jsonify({
                'status': 'success',
                'message': 'Face reference tidak ditemukan, silahkan upload terlebih dahulu',
                'data': {
                    'has_face_reference': False,
                    'uuid': uuid
                }
            }), 200

        # Cek apakah folder ada file gambar (minimal 1 file)
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        has_face = len(files) > 0

        if has_face:
            return jsonify({
                'status': 'success',
                'message': 'Face reference ditemukan',
                'data': {
                    'has_face_reference': True,
                    'uuid': uuid,
                    'files': files
                }
            }), 200
        else:
            return jsonify({
                'status': 'success',
                'message': 'Face reference tidak ditemukan, silahkan upload terlebih dahulu',
                'data': {
                    'has_face_reference': False,
                    'uuid': uuid
                }
            }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Gagal mengecek face reference di folder',
            'error': str(e),
            'data': None
        }), 500

            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Gagal mengecek face reference',
            'error': str(e),
            'data': None
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')

    # 1. Ambil user dari user-service
    user_service_url = f"{Config.USER_SERVICE_URL}/internal/user-by-email?email={email}"
    user_response = requests.get(user_service_url)

    if user_response.status_code != 200:
        return jsonify({"error": "User not found"}), 404

    user = user_response.json()
    password_user = user.get('password')
    is_verified = user.get('is_verified')
    user_id = user.get('id')
    role_id = user.get('role_id')
    uuid = user.get('uuid')

    if not bcrypt.check_password_hash(password_user, password):
        return jsonify({"error": "Invalid credentials"}), 401

    if not is_verified:
        return jsonify({"error": "Email not verified"}), 401

    # 2. Ambil permissions dari role-management-service
    role_service_url = f"{Config.ROLE_SERVICE_URL}/internal/role-name-by-role-id?role_id={role_id}"
    role_response = requests.get(role_service_url)

    # if role_response.status_code != 200:
    #     return jsonify({"error": "Failed to fetch permissions"}), 500

    role_name = role_response.json().get("role_name")

    # 3. Tambahkan custom claims ke JWT
    additional_claims = {
        "role_name": role_name,
        "uuid": uuid,
        "role_id": role_id,
    }

    access_token = create_access_token(
    identity=str(user_id),
    additional_claims=additional_claims
)
    response = {
        "access_token": access_token,
        "refresh_token": create_refresh_token(identity=str(user_id)),
    }

    return jsonify(response), 200
    
    
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
    selected_face_model = data.get('face_model_preference')

    if not email or not face:
        return jsonify({"error": "Email and face image are required"}), 400

    # Ambil user berdasarkan email
    user_service_url = f"{Config.USER_SERVICE_URL}/internal/user-by-email?email={email}"
    user_response = requests.get(user_service_url)

    if user_response.status_code != 200:
        return jsonify({"error": "User not found"}), 404

    user = user_response.json()
    user_id = user['id']
    uuid = user['uuid']
    role_id = user['role_id']
    is_verified = user.get('is_verified')
    user_model_preference = user.get('face_model_preference')
    
    if not is_verified:
        return jsonify({"error": "Email not verified"}), 401

    result, status_code = verify_face_logic(uuid, face, selected_face_model)

    if result.get('match'):
        role_service_url = f"{Config.ROLE_SERVICE_URL}/internal/role-name-by-role-id?role_id={role_id}"
        role_response = requests.get(role_service_url)

        # if role_response.status_code != 200:
        #     return jsonify({"error": "Failed to fetch permissions"}), 500

        role_name = role_response.json().get("role_name")

    # 3. Tambahkan custom claims ke JWT
        additional_claims = {
        "role_name": role_name,
        "uuid": uuid,
        "role_id": role_id,
     }

        access_token = create_access_token(
        identity=str(user_id),
        additional_claims=additional_claims
        )

        if selected_face_model != user_model_preference:
            update_model_url = f"{Config.USER_SERVICE_URL}/update/face-model-preference"
            update_model_response = requests.post(
                update_model_url,
                data={"user_id": user_id, "face_model_preference": selected_face_model},
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            result_model = update_model_response.json()
            if update_model_response.status_code != 200:
                return jsonify(result_model), 500

        response = {
        "access_token": access_token,
        "verification_result": result,
        "refresh_token": create_refresh_token(identity=str(user_id))
    }
        return jsonify(response), 200

    return jsonify({"error": "Face recognition failed", "details": result}), status_code



