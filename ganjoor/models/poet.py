# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT

from inflection import underscore
import requests
from config.settings import ganjoor_base_url
from ganjoor.exceptions import GanjoorException
from . import category


class Poet:
    _urls = {
        "all": "/api/ganjoor/poets",
        "find": "/api/ganjoor/poet/{id}",
        "find_url": "/api/ganjoor/poet"
    }

    def __init__(self, poet_args) -> None:
        for key in poet_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, poet_args[key])

    @classmethod
    def all(cls) -> list():
        path = ganjoor_base_url+cls._urls['all']
        response = requests.get(path)
        if response.status_code == 200:
            body = response.json()
            poets = []
            for entry in body:
                poet = Poet(entry)
                poets.append(poet)
            return poets
        else:
            raise GanjoorException(
                f"Invalid Response Code: {response.status_code} with Message: {response.reason}")

    @classmethod
    def find(cls, id: int):
        path = ganjoor_base_url+cls._urls['find'].format(id=id)
        response = requests.get(path)
        if response.status_code == 200:
            body_poet = response.json()['poet']
            body_cat = response.json()['cat']
            poet = Poet(body_poet)
            poet.categories = category.Category(body_cat)
            return poet
        else:
            raise GanjoorException(
                f"Invalid Response Code: {response.status_code} with Message: {response.reason}")

    @classmethod
    def findByUrl(cls, url):
        path = ganjoor_base_url+cls._urls['find_url']
        response = requests.get(path, params={'url': url})
        if response.status_code == 200:
            body_poet = response.json()['poet']
            body_cat = response.json()['cat']
            poet = Poet(body_poet)
            poet.categories = category.Category(body_cat)
            return poet
        else:
            raise GanjoorException(
                f"Invalid Response Code: {response.status_code} with Message: {response.reason}")

    @property
    def avatar(self, format="png"):
        return ganjoor_base_url+self.image_url

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def full_url(self):
        return self._full_url

    @property
    def root_cat_id(self):
        return self._root_cat_id

    @property
    def nickname(self):
        return self._nickname

    @property
    def published(self):
        return self._published

    @property
    def category(self):
        return self._cat
