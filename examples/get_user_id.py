import os

from instagram.instagram import Instagram


if __name__ == "__main__":
    username = os.environ.get("INSTAGRAM_USERNAME")
    password = os.environ.get("INSTAGRAM_PASSWORD")
    instance = Instagram(username=username, password=password)
    instance.user.login()

    user_id = instance.user.get_userid_from_username(username="testedeinsta202009")
    print(user_id)
