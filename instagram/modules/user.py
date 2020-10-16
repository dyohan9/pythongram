import hashlib
import json

from instagram.modules.connection import Connection
from instagram.utils import Utils


class User(Connection):
    def __init__(self, session, username, password):
        super().__init__(session=session)
        self.username = username
        self.password = password
        self.is_logged_in = None
        self.user_id = None
        self.rank_token = None
        self.token = None
        self.device_id = None
        self.uuid = Utils.generate_uuid(True)

    def search_username(self, username):
        query = self.send_request(f"users/{username}/usernameinfo/")
        return query

    def get_userid_from_username(self, username):
        if "user" in self.search_username(username):
            return str(self.get_last_json.get("user", {}).get("pk"))
        return None  # Not found

    def login(self, force=False):
        m = hashlib.md5()
        m.update(self.username.encode("utf-8") + self.password.encode("utf-8"))
        self.device_id = Utils.generate_devide_id(m.hexdigest())

        if not self.is_logged_in or force:
            # if you need proxy make something like this:
            # self.session.proxies = {"https" : "http://proxyip:proxyport"}
            if self.send_request(
                endpoint=f"si/fetch_headers/?challenge_type=signup&guid={Utils.generate_uuid(False)}"
            ):

                data = {
                    "phone_id": Utils.generate_uuid(True),
                    "_csrftoken": self.get_last_response.cookies["csrftoken"],
                    "username": self.username,
                    "guid": self.uuid,
                    "device_id": self.device_id,
                    "password": self.password,
                    "login_attempt_count": "0",
                }

                if self.send_request(
                    endpoint="accounts/login/",
                    post=Utils.generate_signature(json.dumps(data)),
                ):
                    self.is_logged_in = True
                    self.user_id = self.get_last_json.get("logged_in_user", {}).get(
                        "pk"
                    )
                    self.rank_token = f"{self.user_id}_{self.uuid}"
                    self.token = self.get_last_response.cookies["csrftoken"]

                    print("Login success!")
                    return True
                else:
                    raise Exception("Login or password is incorrect.")
