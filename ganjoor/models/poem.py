# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT


import requests


class Poem:
    def __init__(self, id) -> None:
        self.id = id

    def info(self):
        pass

    @classmethod
    def get_user_bookmarked_poems(cls, auth_token):
        response = requests.get(
            "https://ganjgah.ir/api/ganjoor/bookmark",
            headers={'Authorization': 'bearer '+auth_token})
