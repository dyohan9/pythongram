import requests

from instagram.modules.user import User


class Instagram:
    def __init__(self, username, password):
        self.session = requests.Session()
        self.user = User(session=self.session, username=username, password=password)
