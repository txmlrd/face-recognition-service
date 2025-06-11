import requests
import os
from dotenv import load_dotenv
load_dotenv()

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")

def get_user_by_email(email):
    try:
        resp = requests.get(f"{USER_SERVICE_URL}/internal/user-by-email", params={"email": email})
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print("Error contacting user service:", e)
    return None
