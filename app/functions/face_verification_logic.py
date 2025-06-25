import os
import uuid
from app.models.face_reference import FaceReference
from app.utils.verify_image import FaceVerifier
import logging


def verify_face_logic(uuid_str, uploaded_image_file, model):
    try:
        model = int(model)
    except ValueError:
        return {"error": "Invalid model selected"}, 400

    # ✅ Gunakan nama file unik
    temp_filename = f"temp_upload_{uuid.uuid4().hex}.jpg"
    img_upload_path = os.path.join("temp_uploads", temp_filename)

    # Pastikan folder temp_uploads ada
    os.makedirs("temp_uploads", exist_ok=True)

    # Simpan gambar
    uploaded_image_file.save(img_upload_path)

    try:
        user = FaceReference.query.filter_by(uuid=uuid_str).first()
        if not user:
            return {"error": "User not found"}, 404

        images_path = user.image_path
        reference_images = [
            f"{images_path}/img_{i}.jpg"
            for i in range(1, 4)
            if os.path.exists(f"{images_path}/img_{i}.jpg")
        ]

        if len(reference_images) == 0:
            return {"error": "No reference images found"}, 400

        for ref_img_path in reference_images:
            if model == 1:
                result = FaceVerifier.verify_paper(ref_img_path, img_upload_path)
            elif model == 2:
                result = FaceVerifier.verify_default(ref_img_path, img_upload_path)
            else:
                return {"error": "Invalid model selected"}, 400

            if result.get("verified") is True:
                return {
                    "message": "Match found",
                    "reference_image": ref_img_path,
                    "match": True,
                    "detail": result
                }, 200

        return {
            "message": "No match found in any reference images",
            "match": False
        }, 404

    finally:
        # ✅ Pastikan file selalu dihapus, bahkan jika ada error di atas
        if os.path.exists(img_upload_path):
            os.remove(img_upload_path)
