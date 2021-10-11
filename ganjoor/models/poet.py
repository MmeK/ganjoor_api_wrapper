# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT

import requests
import json
from config.settings import ganjoor_base_url
from ganjoor.exceptions import GanjoorException


class Poet(object):

    _urls = {
        "all": "/api/ganjoor/poets",
        "details": "/api/ganjoor/poet/{}",
        "details_url": "/api/ganjoor/poet",
    }

    def __init__(self, id=None, url=None) -> None:
        self.id = id
        self.url = url
        if (id is None) and (url is None):
            raise GanjoorException("Id and Url not supplied")

    @classmethod
    def all(cls) -> json:
        path = ganjoor_base_url+cls._urls['all']
        response = requests.get(path).json()
        return response

    @classmethod
    def find(cls, id: int) -> json:
        pass

    @classmethod
    def findByUrl():
        pass

    def details(self) -> json:
        if self.id is not None:
            path = ganjoor_base_url+self._urls['details'].format(self.id)
            response = requests.get(
                path, params={'url': self.url})
        else:
            path = ganjoor_base_url+self._urls['details_url']
            response = requests.get(
                path, params={'url': self.url})
        if response.status_code == 200:
            poet = response.json()['poet']
            for key in poet:
                setattr(self, key, poet[key])
            return poet
        else:
            raise GanjoorException(
                f"Invalid Response Code: {response.status_code} with Message: {response.reason}")
