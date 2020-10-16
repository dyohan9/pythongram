import json

from instagram import config


class Connection:
    def __init__(self, session):
        self.__session = session
        self.__last_json = None
        self.__last_response = None

    def send_request(self, endpoint, post=None):
        self.__session.headers.update(
            {
                "Connection": "close",
                "Accept": "*/*",
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie2": "$Version=1",
                "Accept-Language": "en-US",
                "User-Agent": config.USER_AGENT,
            }
        )

        if post != None:  # POST
            response = self.__session.post(
                config.API_URL + endpoint, data=post
            )  # , verify=False
        else:  # GET
            response = self.__session.get(config.API_URL + endpoint)  # , verify=False

        if response.status_code == 200:
            self.__last_response = response
            self.__last_json = json.loads(response.text)
            return True
        else:
            # for debugging
            try:
                self.__last_response = response
                self.__last_json = json.loads(response.text)
            except:
                pass
            raise Exception("Request return " + str(response.status_code) + " error!")

    @property
    def get_last_response(self):
        return self.__last_response

    @property
    def get_last_json(self):
        return self.__last_json
