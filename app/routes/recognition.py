from extensions import os, request, jsonify, Blueprint
from utils.base64 import base64_to_image
from utils.verify_image import verify_images

recognition_bp = Blueprint('recognition', __name__)

@recognition_bp.route('/verify', methods=['POST'])
def verify_route():
    data = request.json

    img1_base64 = data.get("img1")
    img2_base64 = data.get("img2")

    if not img1_base64 or not img2_base64:
        return jsonify({"error": "img1 and img2 fields are required"}), 400

    # Simpan gambar sementara
    img1_path = base64_to_image(img1_base64, "temp1.jpg")
    img2_path = base64_to_image(img2_base64, "temp2.jpg")

    result = verify_images(img1_path, img2_path)

    # Bersihkan file sementara
    try:
        os.remove(img1_path)
        os.remove(img2_path)
    except:
        pass

    return jsonify(result)