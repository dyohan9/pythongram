import os
import requests

from instagram.modules.User import User


class Core:
    def __init__(self):
        self.session = requests.Session()
        self.username = os.environ.get("INSTAGRAM_USERNAME", default=None)
        self.password = os.environ.get("INSTAGRAM_PASSWORD", default=None)
        self.user = User(
            session=self.session, username=self.username, password=self.password
        )


if __name__ == "__main__":
    core = Core()
    core.user.login()

    print(core.user.get_userid_from_username(username="testedeinsta202009"))
