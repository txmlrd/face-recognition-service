# face_verification_logic.py
import os
from app.models.face_reference import FaceReference
from app.utils.verify_image import verify_images # asumsi ini fungsi pembanding wajah

def verify_face_logic(user_id, uploaded_image_file):
    img_upload_path = "temp_upload.jpg"
    uploaded_image_file.save(img_upload_path)

    user = FaceReference.query.filter_by(user_id=user_id).first()
    if not user:
        os.remove(img_upload_path)
        return {"error": "User not found"}, 404

    images_path = user.image_path
    reference_images = [
        f"{images_path}/img_{i}.jpg"
        for i in range(1, 4)
        if os.path.exists(f"{images_path}/img_{i}.jpg")
    ]

    if len(reference_images) == 0:
        os.remove(img_upload_path)
        return {"error": "No reference images found"}, 400

    for ref_img_path in reference_images:
        result = verify_images(ref_img_path, img_upload_path)

        if result.get("verified") is True:
            os.remove(img_upload_path)
            return {
                "message": "Match found",
                "reference_image": ref_img_path,
                "match": True,
                "detail": result
            }, 200

    os.remove(img_upload_path)
    return {
        "message": "No match found in any reference images",
        "match": False
    }, 404
