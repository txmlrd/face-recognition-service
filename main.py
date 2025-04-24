from flask import Flask, request, jsonify
import base64
from PIL import Image
from io import BytesIO
import os
from deepface import DeepFace

app = Flask(__name__)

def base64_to_image(base64_string, filename):
    if base64_string.startswith("data:image"):
        base64_string = base64_string.split(",")[1]  #delete header data
    img_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(img_data))
    image.save(filename)
    return filename

# recognize face
def verify_images(img1, img2):
    try:
        result = DeepFace.verify(
            img1_path=img1,
            img2_path=img2,
            model_name='Facenet512',
            align=True,
            detector_backend='retinaface',
            distance_metric='euclidean_l2'
        )
        filtered = {
            "detector_backend": result.get("detector_backend"),
            "distance": result.get("distance"),
            "model": result.get("model"),
            "similarity_metric": result.get("similarity_metric"),
            "threshold": result.get("threshold"),
            "time": result.get("time"),
            "verified": result.get("verified")
        }

        return filtered
    except Exception as e:
        return {"error": str(e)}

@app.route('/verify', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
