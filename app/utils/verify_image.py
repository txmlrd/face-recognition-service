from deepface import DeepFace

class FaceVerifier:
    @staticmethod
    def verify_default(img1, img2):
        try:
            result = DeepFace.verify(
                img1_path=img1,
                img2_path=img2,
                model_name='Facenet512',
            )
            return FaceVerifier._format_result(result)
        except Exception as e:
            return {"error": str(e), "verified": False}

    @staticmethod
    def verify_paper(img1, img2):
        try:
            result = DeepFace.verify(
                img1_path=img1,
                img2_path=img2,
                model_name='Facenet512',
                align=True,
                detector_backend='retinaface',
                distance_metric='euclidean_l2'
            )
            return FaceVerifier._format_result(result)
        except Exception as e:
            return {"error": str(e), "verified": False}

    @staticmethod
    def _format_result(result):
        return {
            "detector_backend": result.get("detector_backend"),
            "distance": result.get("distance"),
            "model": result.get("model"),
            "similarity_metric": result.get("similarity_metric"),
            "threshold": result.get("threshold"),
            "time": result.get("time"),
            "verified": result.get("verified")
        }
