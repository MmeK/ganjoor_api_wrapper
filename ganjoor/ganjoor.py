# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
import requests
from config.settings import ganjoor_base_url
from ganjoor.exceptions import GanjoorException

from .models import Poet


# TODO: Fix Logging
# import logging
# from os.path import join as path_join


# import http.client as http_client
# http_client.HTTPConnection.debuglevel = 1

# logging.basicConfig(filename=path_join("logs", "example.log"))
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


class Ganjoor:
    def __init__(self, token=None, language="string", app_name="pythonclient"):
        self.token = token
        self.language = language
        self.app_name = app_name

    def log_in(self, username, password):
        self.username = username
        self.password = password
        response = requests.post(ganjoor_base_url+"/api/users/login",
                                 json={"username": self.username, "password": self.password,
                                       "clientAppName": self.app_name,
                                       "language": self.language})
        if response.status_code == 200:
            self.auth_token = response.json()['token']
        else:
            raise GanjoorException(
                f"""Authentication Failed with Code: {response.status_code},
                 Message: {response.reason}""")

    def get_user_bookmarks(self):
        if self.auth_token is None:
            raise GanjoorException("user is not logged in")
        else:
            pass  # TODO: get Bookmarks

    def find_poet_by_id(self, id: int) -> Poet:
        return Poet.find(id)
