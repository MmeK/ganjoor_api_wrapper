# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from typing import List
import requests
from ganjoor.exceptions import GanjoorException

from .models import Category, Poet, Poem
from . import GANJGAH_BASE_URL
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
    def __init__(self, token=None, language="string", app_name="pythonclient",
                 base_url=GANJGAH_BASE_URL):
        self.token = token
        self.language = language
        self.base_url = base_url
        self.app_name = app_name

    def log_in(self, username, password):
        self.username = username
        self.password = password
        response = requests.post(self.base_url+"/api/users/login",
                                 json={"username": self.username,
                                       "password": self.password,
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

    def find_poet_by_url(self, url: str) -> Poet:
        return Poet.find_by_url(url)

    def find_category_by_id(self, id: int, with_poems=True) -> Category:
        return Category.find(id, with_poems)

    def find_category_by_url(self, url: str, with_poems=True) -> Category:
        return Category.find_by_url(url, with_poems)

    def find_poem_by_id(self, id: int, complete=False, category_info=False,
                        category_poems=False, rhymes=False,
                        recitations=False, images=False,
                        songs=False, comments=False,
                        verse_details=False, navigation=False) -> Poem:
        return Poem.find(id, complete=complete,
                         category_info=category_info,
                         category_poems=category_poems, rhymes=rhymes,
                         recitations=recitations, images=images, songs=songs,
                         comments=comments, verse_details=verse_details,
                         navigation=navigation)

    def find_poem_by_url(self, url: str, complete=False, category_info=False,
                         category_poems=False, rhymes=False,
                         recitations=False, images=False,
                         songs=False, comments=False,
                         verse_details=False, navigation=False) -> Poem:
        return Poem.find_by_url(url=url, complete=complete,
                                category_info=category_info,
                                category_poems=category_poems, rhymes=rhymes,
                                recitations=recitations, images=images, songs=songs,
                                comments=comments, verse_details=verse_details,
                                navigation=navigation)

    def find_random_poem(self, poet_id=None) -> Poem:
        return Poem.random(poet_id=poet_id)

    def find_similar_poems(self, page_size: int = 5, page_number: int = 1,
                           metre: str = None, rhyme: str = None,
                           poet_id=0) -> List[Poem]:
        return Poem.similar(page_number=page_number,
                            page_size=page_size, metre=metre, rhyme=rhyme,
                            poet_id=poet_id)
