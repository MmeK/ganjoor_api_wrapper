# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from __future__ import annotations
from typing import List
from inflection import underscore
import requests
from config.settings import ganjoor_base_url
from ganjoor.exceptions import GanjoorException
import poem
import poet


class Category:

    _urls = {
        "find": "/api/ganjoor/cat/{id}",
        "find_url": "/api/ganjoor/cat"
    }

    def __init__(self, category_args):
        for key in category_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, category_args[key])

    @property
    def children(self) -> List[Category]:
        if self._children:
            return [Category(child) for child in self._children]
        return []

    @property
    def poems(self) -> List[poem.poem.Poem]:
        if self._poems:
            return [poem.Poem(poem) for poem in self._poems]
        return []

    @property
    def next(self) -> Category:
        return Category(self._next)

    @property
    def previous(self) -> Category:
        return Category(self._previous)

    @property
    def ancestors(self) -> List[Category]:
        if self._ancestors:
            return [Category(ancestor) for ancestor in self._ancestors]
        return []

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def url_slug(self) -> str:
        return self._url_slug

    @property
    def full_url(self) -> str:
        return self._full_url

    @classmethod
    def find(cls, id, poems=False) -> Category:
        path = ganjoor_base_url+cls._urls['find'].format(id=id)
        response = requests.get(path, params={'poems': poems})
        if response.status_code == 200:
            body_poet = response.json()['poet']
            body_cat = response.json()['cat']
            category = Category(body_cat)
            category.poet = poet.Poet(body_poet)
            return category
        else:
            raise GanjoorException(
                f"Invalid Response Code: {response.status_code} with Message: {response.reason}")

    @classmethod
    def find_by_url(cls, url, poems=False) -> Category:
        path = ganjoor_base_url+cls._urls['find']
        response = requests.get(path, params={'poems': poems, 'url': url})
        if response.status_code == 200:
            body_poet = response.json()['poet']
            body_cat = response.json()['cat']
            category = Category(body_cat)
            category.poet = poet.Poet(body_poet)
            return category
        else:
            raise GanjoorException(
                f"""Invalid Response Code: {response.status_code}
                Message: {response.reason}""")
