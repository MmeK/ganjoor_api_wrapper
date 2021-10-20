# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from __future__ import annotations
from typing import List
from inflection import underscore
from dataclasses import dataclass
import requests
from config.settings import ganjoor_base_url
from ganjoor.exceptions import GanjoorException
from .poem_utils import (PoemImage, Comment, IncompletePoem,
                         Song, Recitation, Verse, Metre, Couplet)


@dataclass
class Category:

    _id: int
    _title: str
    _url_slug: str
    _full_url: str
    _next: Category
    _previous: Category
    _ancestors: List[Category]
    _children: List[Category]
    _poems: List[Poem]

    __urls = {
        "find": "/api/ganjoor/cat/{id}",
        "find_by_url": "/api/ganjoor/cat"
    }

    def __init__(self, category_args):
        for key in category_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, category_args[key])

    @classmethod
    def find(cls, id, poems=False) -> Category:
        path = ganjoor_base_url+cls.__urls['find'].format(id=id)
        response = requests.get(path, params={'poems': poems})
        if response.status_code == 200:
            body_poet = response.json()['poet']
            body_cat = response.json()['cat']
            category = Category(body_cat)
            category._poet = body_poet
            return category
        else:
            raise GanjoorException(
                f"Invalid Response Code: {response.status_code} with Message: {response.reason}")

    @classmethod
    def find_by_url(cls, url, poems=False) -> Category:
        path = ganjoor_base_url+cls.__urls['find_by_url']
        response = requests.get(path, params={'poems': poems, 'url': url})
        if response.status_code == 200:
            body_poet = response.json()['poet']
            body_cat = response.json()['cat']
            category = Category(body_cat)
            category._poet = body_poet
            return category
        else:
            raise GanjoorException(
                f"""Invalid Response Code: {response.status_code}
                Message: {response.reason}""")

    @property
    def children(self) -> List[Category]:
        if self._children:
            return [Category(child) for child in self._children]
        return []

    @property
    def poems(self) -> List[Poem]:
        if self._poems:
            return [poem.Poem(poem) for poem in self._poems]

        return []

    @property
    def next_category(self) -> Category:
        return Category(self._next)

    @property
    def previous_category(self) -> Category:
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

    @property
    def poet(self) -> Poet:
        return Poet(self._poet)


@dataclass
class Poet:

    _id: int
    _name: str
    _description: str
    _full_url: str
    _root_cat_id: int
    _nickname: str
    _published: bool
    _image_url: str
    _cat: Category = None

    __urls = {
        "all": "/api/ganjoor/poets",
        "find": "/api/ganjoor/poet/{id}",
        "find_by_url": "/api/ganjoor/poet"
    }

    def __init__(self, poet_args) -> None:
        for key in poet_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, poet_args[key])

    @classmethod
    def all(cls) -> list():
        path = ganjoor_base_url+cls.__urls['all']
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
        path = ganjoor_base_url+cls.__urls['find'].format(id=id)
        response = requests.get(path)
        if response.status_code == 200:
            body_poet = response.json()['poet']
            body_cat = response.json()['cat']
            poet = Poet(body_poet)
            poet._cat = body_cat
            return poet
        else:
            raise GanjoorException(
                f"Invalid Response Code: {response.status_code} with Message: {response.reason}")

    @classmethod
    def find_by_url(cls, url):
        path = ganjoor_base_url+cls.__urls['find_by_url']
        response = requests.get(path, params={'url': url})
        if response.status_code == 200:
            body_poet = response.json()['poet']
            body_cat = response.json()['cat']
            poet = Poet(body_poet)
            poet._cat = body_cat
            return poet
        else:
            raise GanjoorException(
                f"Invalid Response Code: {response.status_code} with Message: {response.reason}")

    @property
    def avatar_url(self, format="png") -> str:
        return ganjoor_base_url+self.image_url

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def full_url(self) -> str:
        return self._full_url

    @property
    def root_cat_id(self) -> int:
        return self._root_cat_id

    @property
    def nickname(self) -> str:
        return self._nickname

    @property
    def published(self) -> bool:
        return self._published

    @property
    def category(self) -> Category:
        return Category(self._cat)


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
    _category: Category
    _next: IncompletePoem
    _previous: IncompletePoem
    _verses: List[Verse]
    _recitations: List[Recitation]
    _images: List[PoemImage]
    _songs: List[Song]
    _comments: List[Comment]
    _poet: Poet

    __urls = {
        "find": "/api/ganjoor/poem/{id}",
        "find_by_url": "/api/ganjoor/poem",
        "recitations": "/recitations",
        "images": "/images",
        "songs": "/songs",
        "comments": "/comments",
        "hafez_faal": "/api/ganjoor/hafez/faal"
    }

    def __init__(self, poem_args) -> None:
        for key in poem_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, poem_args[key])
        if self._category:
            self._poet = Poet(self._category['poet'])
            self._category = Category(self._category['cat'])

    @classmethod
    def find(cls, id, complete=False, category_info=False, category_poems=False, rhymes=False,
             recitations=False, images=False, songs=False, comments=False,
             verse_details=False, navigation=False) -> Poem:
        params = dict.copy(locals())
        params.pop('id')
        if complete:
            for key in params.keys():
                params[key] = True
        path = ganjoor_base_url+cls.__urls['find'].format(id=id)
        response = requests.get(path, params=params)
        if response.status_code == 200:
            body = response.json()
            return Poem(body)
        else:
            raise GanjoorException(
                f"Invalid Response Code: {response.status_code} with Message: {response.reason}")

    @classmethod
    def find_by_url(cls, url, category_info=False, category_poems=False,
                    rhymes=False, recitations=False, images=False, songs=False,
                    comments=False, verse_details=False,
                    navigation=False) -> Poem:
        params = dict.copy(locals())
        path = ganjoor_base_url+cls.__urls['find_by_url']
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

    @classmethod
    def hafez_faal(cls):
        path = ganjoor_base_url+cls.__urls['hafez_faal']
        response = requests.get(path)
        if response.status_code == 200:
            body = response.json()
            return Poem(body)
        else:
            raise GanjoorException(
                f"Invalid Response Code: {response.status_code} with Message: {response.reason}")

    def request_recitations(self) -> List[Recitation]:
        path = ganjoor_base_url + \
            self.__urls['find'].format(id=self.id)+self.__urls['recitations']
        response = requests.get(path)
        if response.status_code == 200:
            body = response.json()
            return [Recitation(recitation) for recitation in body]
        else:
            raise GanjoorException(
                f"Invalid Response Code: {response.status_code} with Message: {response.reason}")

    def request_images(self) -> List[PoemImage]:
        path = ganjoor_base_url + \
            self.__urls['find'].format(id=self.id)+self.__urls['images']
        response = requests.get(path)
        if response.status_code == 200:
            body = response.json()
            return [PoemImage(image) for image in body]
        else:
            raise GanjoorException(
                f"Invalid Response Code: {response.status_code} with Message: {response.reason}")

    def request_songs(self, track_type=-1, approved=True) -> List[Song]:
        path = ganjoor_base_url + \
            self.__urls['find'].format(id=self.id)+self.__urls['songs']
        response = requests.get(
            path, params={'track_type': track_type, 'approved': approved})
        if response.status_code == 200:
            body = response.json()
            return [Song(song) for song in body]
        else:
            raise GanjoorException(
                f"Invalid Response Code: {response.status_code} with Message: {response.reason}")

    def request_comments(self) -> List[Comment]:
        path = ganjoor_base_url + \
            self.__urls['find'].format(id=self.id)+self.__urls['comments']
        response = requests.get(path)
        if response.status_code == 200:
            body = response.json()
            return [Comment(comment) for comment in body]
        else:
            raise GanjoorException(
                f"Invalid Response Code: {response.status_code} with Message: {response.reason}")

    def get_couplet(self, index: int) -> Couplet:
        return Couplet([verse for verse in self.verses
                        if verse.couplet_index == index])

    def get_all_couplets(self) -> List[Couplet]:
        last_couplet = max([verse.couplet_index for verse in self.verses])
        return [self.get_couplet(index)
                for index in range(0, last_couplet+1)]

    def __str__(self):
        all_couplets = self.get_all_couplets()
        return '\n\n'.join([str(couplet) for couplet in all_couplets])

    @property
    def ganjoor_metre(self) -> Metre:
        return Metre(self._ganjoor_metre)

    @property
    def category(self) -> Category:
        return self._category

    @property
    def poet(self) -> Poet:
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
        return IncompletePoem(self._previous) if self._previous else None

    @property
    def next_poem(self) -> IncompletePoem:
        return IncompletePoem(self._next) if self._next else None

    @property
    def normal_image_urls(self) -> List[str]:
        return [poem_image.normal_image_url for poem_image in self.images]

    @property
    def thumbnail_urls(self) -> List[str]:
        return [poem_image.thumbnail_image_url for poem_image in self.images]

    @property
    def verses(self) -> List[Verse]:
        return [Verse(verse) for verse in self._verses]

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
