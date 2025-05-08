from extensions import os, request, jsonify, Blueprint, DeepFace
from utils.verify_image import verify_images
import os

recognition_bp = Blueprint('recognition', __name__)

@recognition_bp.route('/verify', methods=['POST'])
def verify_route():
    # Ambil data dari form
    img_upload = request.files.get("image")
    user_id = request.form.get("user_id")

    if not img_upload or not user_id:
        return jsonify({"error": "image and user_id are required"}), 400

    # Simpan gambar upload sementara
    img_upload_path = "temp_upload.jpg"
    img_upload.save(img_upload_path)

    # Ambil 3 foto referensi dari storage
    reference_images = []
    for i in range(1, 4):
        ref_img_path = f"storage/faces/{user_id}/img_{i}.jpg"
        if os.path.exists(ref_img_path):
            reference_images.append(ref_img_path)

    if len(reference_images) == 0:
        os.remove(img_upload_path)
        return jsonify({"error": "No reference images found for this user"}), 400

    # Bandingkan satu per satu
    for ref_img_path in reference_images:
        result = verify_images(ref_img_path, img_upload_path)

        print(f"[DEBUG] Comparing with: {ref_img_path}")
        print(f"[DEBUG] Distance: {result.get('distance')} | Threshold: {result.get('threshold')} | Verified: {result.get('verified')}")

        if result.get("verified") is True:
            os.remove(img_upload_path)
            return jsonify({
                "message": "Match found",
                "reference_image": ref_img_path,
                "match": True,
                "detail": result  # Bisa dihapus kalau gak mau tampilkan detail
            })

    # Kalau tidak ada yang cocok
    os.remove(img_upload_path)
    return jsonify({
        "message": "No match found in any reference images",
        "match": False
    }), 404
