# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT

from pytest import fixture
from ganjoor_wrapper import Poet
import vcr


class TestPoet:

    @fixture
    def poet_keys(self):
        return ['id', 'name', 'description', 'fullUrl', 'rootCatId',
                'nickname', 'published', 'imageUrl']

    @vcr.use_cassette('tests/vcr_cassettes/poet_details.yml')
    def test_poet_details(self, poet_keys):
        """Tests an API call to get a Poet's details"""
        poet_instance = Poet(57)
        response = poet_instance.details()
        assert isinstance(response, dict)
        assert response['id'] == 57, "The ID should be in the response"
        assert set(poet_keys).issubset(response.keys()
                                       ), "All keys should be in the response"

    @vcr.use_cassette('tests/vcr_cassettes/poet_details_url.yml')
    def test_poet_details_url(self, poet_keys):
        """Tests an API call to get a Poet's details using its url"""
        poet_instance = Poet(url="/hafezasdasdasdasd")
        response = poet_instance.details()
        assert isinstance(response, dict)
        assert response['fullUrl'] == '/hafez', "The ID should be in the response"
        assert set(poet_keys).issubset(response.keys()
                                       ), "All keys should be in the response"

    @vcr.use_cassette('tests/vcr_cassettes/poets_all.yml')
    def test_poet_all(self, poet_keys):
        poets = Poet.all()
        assert isinstance(poets, list)
        for poet in poets:
            assert set(poet_keys).issubset(
                poet.keys()), "All keys should be in response"
