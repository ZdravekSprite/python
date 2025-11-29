# teltonika_client.py
import requests
from config import FOTA_API_TOKEN

class TeltonikaAPI:
    BASE_URL = "https://api.teltonika.lt"

    def __init__(self, token=None):
        self.token = token or FOTA_API_TOKEN
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def _request(self, method, endpoint, **kwargs):
        url = self.BASE_URL + endpoint
        resp = requests.request(method, url, headers=self.headers, **kwargs)
        if resp.status_code >= 400:
            raise Exception(f"{resp.status_code}: {resp.text}")
        return resp.json()

    def get_devices(self, page=1):
        return self._request("GET", f"/devices?page={page}")

    def get_all_devices(self):
        devices = []
        page = 1
        while True:
            result = self.get_devices(page)
            data = result.get("data", [])
            devices.extend(data)
            if page >= result.get("last_page", 1):
                break
            page += 1
        return devices
