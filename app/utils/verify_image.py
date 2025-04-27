from extensions import DeepFace

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