# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT

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
            setattr(self, snake_key, poet_args[key])

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

    def get_avatar(self, format="png"):
        return ganjoor_base_url+self.image_url


class Category:

    _urls = {
        "find": "/api/ganjoor/cat/{id}",
        "find_url": "/api/ganjoor/cat"
    }

    def __init__(self, category_args):
        for key in category_args.keys():
            snake_key = underscore(key)
            setattr(self, snake_key, category_args[key])
        if self.children is not None:
            children = []
            for child in self.children:
                children.append(Category(child))
            self.children = children
        if self.poems is not None:
            poems = []
            for poem in self.poems:
                poems.append(Poem(poem))
            self.poems = poems
        if self.next is not None:
            self.next = Category(self.next)
        if self.previous is not None:
            self.previous = Category(self.previous)
        if self.ancestors is not None:
            ancestors = []
            for ancestor in self.ancestors:
                ancestors.append(Category(ancestor))
            self.ancestors = ancestors

    @classmethod
    def find(cls, id, poems=False):
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
    def find_by_url(cls, url, poems=False):
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
            setattr(self, snake_key, poem_args[key])
        if self.ganjoor_metre is not None:
            self.ganjoor_metre = Metre(self.ganjoor_metre)
        if self.category is not None:
            self.poet = Poet(self.category['poet'])
            self.category = Category(self.category['cat'])
        if self.next is not None:
            self.__next = self.next
            del self.next
        if self.previous is not None:
            self.__previous = self.previous
            del self.__previous

    @classmethod
    def find(cls, id, category_info=True, category_poems=True, rhymes=True,
             recitations=True, images=True, songs=True, comments=False,
             verse_details=True, navigation=True):
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

    @classmethod
    def get_user_bookmarked_poems(cls, auth_token):
        response = requests.get(
            "https://ganjgah.ir/api/ganjoor/bookmark",
            headers={'Authorization': 'bearer '+auth_token})

    def get_previous_poem(self):
        return Poem.find(self.__previous['id'])

    def get_next_poem(self):
        return Poem.find(self.__next['id'])


class Metre:
    def __init__(self, metre_args) -> None:
        for key in metre_args.keys():
            snake_key = underscore(key)
            setattr(self, snake_key, metre_args[key])
