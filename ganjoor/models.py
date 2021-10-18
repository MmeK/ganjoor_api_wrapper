# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from __future__ import annotations
from dataclasses import dataclass
from typing import List
from inflection import underscore
import requests
from config.settings import ganjoor_base_url
from ganjoor.exceptions import GanjoorException


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
            poet.categories = Category(body_cat)
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
            poet.categories = Category(body_cat)
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
    def poems(self) -> List[Poem]:
        if self._poems:
            return [Poem(poem) for poem in self._poems]
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
            category.poet = Poet(body_poet)
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
            category.poet = Poet(body_poet)
            return category
        else:
            raise GanjoorException(
                f"""Invalid Response Code: {response.status_code}
                Message: {response.reason}""")


class Poem:

    # Metre, Cat, Nav(next,prev), Verses, Recitations, Images, Songs, Comments
    __urls = {
        "find": "/api/ganjoor/poem/{id}",
        "find_url": "/api/ganjoor/poem"
    }

    def __init__(self, poem_args) -> None:
        for key in poem_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, poem_args[key])
        if self._category:
            self._poet = Poet(self.category['poet'])
            self._category = Category(self.category['cat'])

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


class Metre:
    def __init__(self, metre_args) -> None:
        for key in metre_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, metre_args[key])

    @property
    def id(self) -> int:
        return self._id

    @property
    def url_slug(self) -> str:
        return self._url_slug

    @property
    def rhythm(self) -> str:
        return self._rhythm

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def verse_count(self) -> int:
        return self._verse_count


class PoemImage:
    def __init__(self, poem_image_args) -> None:
        for key in poem_image_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, poem_image_args[key])

    @property
    def normal_image_url(self) -> str:
        return self.thumbnail_image_url.replace('thumb', 'normal')

    @property
    def image_order(self) -> int:
        return self._image_order

    @property
    def poem_related_image_type(self) -> int:
        return self._poem_related_image_type

    @property
    def thumbnail_image_url(self) -> str:
        return self._thumbnail_image_url

    @property
    def target_page_url(self) -> str:
        return self._target_page_url

    @property
    def alt_text(self) -> str:
        return self._alt_text


@dataclass
class Verse:
    _id: int
    _v_order: int
    _couplet_index: int
    _verse_position: int
    _text: str

    def __init__(self, verse_args):
        for key in verse_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, verse_args[key])

    @property
    def id(self) -> int:
        return self._id

    @property
    def v_order(self) -> int:
        return self._v_order

    @property
    def couplet_index(self) -> int:
        return self._couplet_index

    @property
    def verse_position(self) -> int:
        return self._verse_position

    @property
    def text(self) -> str:
        return self._text


@dataclass
class Couplet:
    _verses: List[Verse]

    @property
    def verses(self) -> List[Verse]:
        return self._verses

    def __str__(self):
        return '\n'.join([verse.text for verse in self.verses])


@dataclass
class Song:
    _id: int
    _poem_id: int
    _track_type: int
    _artist_name: str
    _artist_url: str
    _album_name: str
    _album_url: str
    _track_name: str
    _track_url: str
    _description: str
    _broken_link: bool
    _golha_track_id: int
    _approved: int
    _rejected: int
    _rejected_cause: str
    _suggested_by_id: str
    _suggested_by_nickname: str

    def __init__(self, song_args):
        for key in song_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, song_args[key])


@dataclass
class Comment:
    _id: int
    _author_name: str
    _author_url: str
    _comment_date: str
    _html_comment: str
    _publish_status: str
    _in_reply_to_id: int
    _user_id: int
    _replies: List[Comment]
    _my_comment: bool
    _couplet_index: int
    _couplet_summary: str

    def __init__(self, comment_args):
        for key in comment_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, comment_args[key])

    @property
    def replies(self):
        return [Comment(comment) for comment in self._replies]


@dataclass
class Recitation:
    _id: int
    _poem_id: int
    _poem_full_title: str
    _poem_full_url: str
    _audio_title: str
    _audio_artist: str
    _audio_artist_url: str
    _audio_src: str
    _audio_src_url: str
    _legacy_audio_guid: str
    _mp3_file_check_sum: str
    _mp3_size_in_bytes: int
    _publish_date: str
    _file_last_updated: str
    _mp3_url: str
    _xml_text: str
    _plain_text: str
    _html_text: str

    def __init__(self, recitation_args):
        for key in recitation_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, recitation_args[key])
