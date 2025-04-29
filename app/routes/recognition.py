from extensions import os, request, jsonify, Blueprint
from utils.base64 import base64_to_image
from utils.verify_image import verify_images
import os

recognition_bp = Blueprint('recognition', __name__)

@recognition_bp.route('/verify', methods=['POST'])
def verify_route():
    # Ambil data yang dikirim via form-data
    img_upload = request.files.get("image")
    user_id = request.form.get("user_id")

    if not img_upload or not user_id:
        return jsonify({"error": "image and user_id are required"}), 400

    # Simpan gambar sementara
    img_upload_path = "temp_upload.jpg"
    img_upload.save(img_upload_path)

    # Ambil 3 foto referensi yang sudah disimpan di folder storage
    reference_images = []
    for i in range(1, 4):
        ref_img_path = f"storage/faces/{user_id}/img_{i}.jpg"
        if os.path.exists(ref_img_path):
            reference_images.append(ref_img_path)

    if len(reference_images) == 0:
        return jsonify({"error": "No reference images found for this user"}), 400

    # Verifikasi foto upload terhadap tiap foto referensi
    result = {"matches": []}
    match_found = False
    for ref_img_path in reference_images:
        match = verify_images(ref_img_path, img_upload_path)
        result["matches"].append({
            "reference_image": ref_img_path,
            "match": match
        })
        
        # Jika sudah ada yang cocok (match == True), hentikan iterasi dan keluar
        if match:
            return jsonify({
                "message": "Match found",
                "reference_image": ref_img_path,
                "match": True
            })

    # Jika tidak ada yang match setelah iterasi semua gambar
    return jsonify({
        "message": "No match found in any reference images",
        "matches": result["matches"]
    }), 404

    # Bersihkan file sementara
    try:
        os.remove(img_upload_path)
    except:
        pass
