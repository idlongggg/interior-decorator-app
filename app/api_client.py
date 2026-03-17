import os
import requests
import streamlit as st

class APIClient:
    def __init__(self, base_url: str = None):
        if base_url is None:
            self.base_url = os.getenv("API_URL", "http://localhost:8001")
        else:
            self.base_url = base_url

    def upload_image(self, image_file):
        files = {"file": (image_file.name, image_file.getvalue(), image_file.type)}
        try:
            response = requests.post(f"{self.base_url}/upload", files=files)
            if response.status_code == 200:
                return response.json()["image_path"]
        except Exception as e:
            st.error(f"Upload error: {e}")
        return None

    def trigger_generation(self, image_path, style, room_type, custom_prompt):
        payload = {
            "image_path": image_path,
            "style": style,
            "room_type": room_type,
            "custom_prompt": custom_prompt
        }
        try:
            response = requests.post(f"{self.base_url}/generate", json=payload)
            if response.status_code == 200:
                return response.json()["task_id"]
        except Exception as e:
            st.error(f"Generation trigger error: {e}")
        return None

    def get_status(self, task_id):
        try:
            response = requests.get(f"{self.base_url}/status/{task_id}")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            st.error(f"Status check error: {e}")
        return None

    def get_result_url(self, relative_url):
        return f"{self.base_url}{relative_url}"

    def get_docs_url(self):
        return f"{self.base_url}/docs"

api_client = APIClient()
