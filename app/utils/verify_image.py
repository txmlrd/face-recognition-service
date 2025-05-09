from deepface import DeepFace
import os

def verify_images(img1, img2):
    try:
        # print("[DEBUG] img1:", img1, "| exists:", os.path.exists(img1))
        # print("[DEBUG] img2:", img2, "| exists:", os.path.exists(img2))

        result = DeepFace.verify(
            img1_path=img1,
            img2_path=img2,
            model_name='Facenet512',
            align=True,
            detector_backend='retinaface',
            distance_metric='euclidean_l2'
        )
        return {
            "detector_backend": result.get("detector_backend"),
            "distance": result.get("distance"),
            "model": result.get("model"),
            "similarity_metric": result.get("similarity_metric"),
            "threshold": result.get("threshold"),
            "time": result.get("time"),
            "verified": result.get("verified")
        }
    except Exception as e:
        # print("[ERROR]", str(e))
        return {"error": str(e), "verified": False}

