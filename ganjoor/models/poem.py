# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT

from __future__ import annotations
from typing import List
from inflection import underscore
from dataclasses import dataclass
import requests
from config.settings import ganjoor_base_url
from ganjoor.exceptions import GanjoorException
import category
import poet
from poem_utils import (Verse, Comment, Couplet,
                        Recitation, Metre, PoemImage, Song)


@dataclass
class Poem:

    __urls = {
        "find": "/api/ganjoor/poem/{id}",
        "find_url": "/api/ganjoor/poem"
    }

    def __init__(self, poem_args) -> None:
        for key in poem_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, poem_args[key])
        if self._category:
            self._poet = poet.Poet(self.category['poet'])
            self._category = category.Category(self.category['cat'])

        if self._next:
            self.__next = self._next
            del self._next

        if self._previous:
            self.__previous = self._previous
            del self._previous

    @classmethod
    def find(cls, id, category_info=True, category_poems=True, rhymes=True,
             recitations=True, images=True, songs=True, comments=True,
             verse_details=True, navigation=True) -> Poem:
        params = dict.copy(locals())
        params.pop('id')
        path = ganjoor_base_url+cls.__urls['find'].format(id=id)
        response = requests.get(path, params=params)
        if response.status_code == 200:
            body = response.json()
            return Poem(body)
        else:
            raise GanjoorException(
                f"Invalid Response Code: {response.status_code} with Message: {response.reason}")

    # @classmethod
    # def get_user_bookmarked_poems(cls, auth_token):
    #     response = requests.get(
    #         "https://ganjgah.ir/api/ganjoor/bookmark",
    #         headers={'Authorization': 'bearer '+auth_token})
    @property
    @property
    def ganjoor_metre(self) -> Metre:
        return Metre(self._ganjoor_metre)

    @property
    def category(self) -> category.Category:
        return self._category

    @property
    def poet(self) -> poet.Poet:
        return self._poet

    @property
    def recitations(self) -> List[Recitation]:
        if self._recitations:
            return [Recitation(recitation) for recitation in self._recitations]
        return []

    @property
    def songs(self) -> List[Song]:
        if self._songs:
            return [Song(song) for song in self._songs]
        return []

    @property
    def comments(self) -> List[Comment]:
        if self._comments:
            return [Comment(comment) for comment in self._comments]
        return []

    @property
    def images(self) -> List[PoemImage]:
        return [PoemImage(image) for image in self._images]

    @property
    def previous_poem(self) -> Poem:
        return Poem.find(self.__previous['id'])

    @property
    def next_poem(self) -> Poem:
        return Poem.find(self.__next['id'])

    @property
    def normal_image_urls(self) -> List[str]:
        return [poem_image.normal_image_url for poem_image in self.images]

    @property
    def thumbnail_urls(self) -> List[str]:
        return [poem_image.thumbnail_image_url for poem_image in self.images]

    @property
    def verses(self) -> List[Verse]:
        return [Verse(verse) for verse in self._verses]

    def get_couplet(self, index: int) -> Couplet:
        return Couplet([verse for verse in self.verses if verse.couplet_index == index])

    def get_all_couplets(self) -> List[Couplet]:
        last_couplet = max([verse.couplet_index for verse in self.verses])
        return [self.get_couplet(index)
                for index in range(0, last_couplet+1)]

    def __str__(self):
        all_couplets = self.get_all_couplets()
        return '\n\n'.join([str(couplet) for couplet in all_couplets])
