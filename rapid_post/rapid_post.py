import requests

from rapid_db_creation import RapidDB


class RapidPost:
    def __init__(self, url=None, payload=None, request_type=None, auto_rapid_db=False):
        self.url = url
        self.payload = payload
        self.request_type = request_type
        self.auto_rapid_db = auto_rapid_db
        if self.request_type == "POST":
            self._rapid_post_request()

    def _rapid_post_request(self):
        """functionality to create the post request with the corresponding url and the payload"""
        if self.auto_rapid_db == True and isinstance(self.payload, dict):
            rapid_db_instance = RapidDB(db_credentials=self.payload)._rapid_db_create()
        if isinstance(self.payload, dict):
            response = requests.post(self.url, json=self.payload)
            return response.text
        else:
            return dict(status="Failed", message="Payload type is not JSON")
