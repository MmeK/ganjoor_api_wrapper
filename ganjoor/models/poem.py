# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT

from __future__ import annotations
from typing import List
from inflection import underscore
from dataclasses import dataclass
import requests
from config.settings import ganjoor_base_url
from ganjoor.exceptions import GanjoorException
from . import category
from . import poet
from .poem_utils import (Verse, Comment, Couplet,
                         IncompletePoem, Recitation, Metre, PoemImage, Song)


@dataclass
class Poem:
    _id: int
    _title: str
    _full_title: str
    _url_slug: str
    _full_url: str
    _ganjoor_metre: Metre
    _rhyme_letters: str
    _plain_text: str
    _html_text: str
    _source_name: str
    _source_url_slug: str
    _old_tag: str
    _old_tag_page_url: str
    _category: category.Category
    _next_poem: IncompletePoem
    _previous_poem: IncompletePoem
    _verses: List[Verse]
    _recitations: List[Recitation]
    _images: List[PoemImage]
    _songs: List[Song]
    _comments: List[Comment]
    _poet: poet.Poet

    __urls = {
        "find": "/api/ganjoor/poem/{id}",
        "find_url": "/api/ganjoor/poem"
    }

    def __init__(self, poem_args) -> None:
        print("hi")
        for key in poem_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, poem_args[key])
        if self._category:
            self._poet = poet.Poet(self.category['poet'])
            self._category = category.Category(self.category['cat'])

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
    def previous_poem(self) -> IncompletePoem:
        return IncompletePoem(self._previous)

    @property
    def next_poem(self) -> IncompletePoem:
        return IncompletePoem(self._next)

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

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def full_title(self) -> str:
        return self._full_title

    @property
    def url_slug(self) -> str:
        return self._url_slug

    @property
    def full_url(self) -> str:
        return self._full_url

    @property
    def plain_text(self) -> str:
        return self._plain_text

    @property
    def html_text(self) -> str:
        return self._html_text

    @property
    def rhyme_letters(self) -> str:
        return self._rhyme_letters

    @property
    def source_name(self) -> str:
        return self._source_name

    @property
    def source_url_slug(self) -> str:
        return self._source_url_slug

    @property
    def old_tag(self) -> str:
        return self._old_tag

    @property
    def old_tag_page_url(self) -> str:
        return self._old_tag_page_url
