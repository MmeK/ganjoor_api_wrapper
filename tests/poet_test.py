# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT

from pytest import fixture
from ganjoor import Poet
import vcr


class TestPoet:

    @fixture
    def poet_keys(self):
        return ['_id', '_name', '_description', '_full_url', '_root_cat_id',
                '_nickname', '_published', '_image_url']

    @vcr.use_cassette('tests/vcr_cassettes/poet_find.yml')
    def test_poet_find(self, poet_keys):
        """Tests an API call to get a Poet's details"""
        poet_instance = Poet.find(57)
        assert isinstance(poet_instance, Poet)
        assert poet_instance.id == 57, "The ID should be in the poet_instance"
        assert set(poet_keys).issubset(poet_instance.__dict__.keys()
                                       ), "All keys should be in the response"

    @vcr.use_cassette('tests/vcr_cassettes/poet_find_url.yml')
    def test_poet_find_by_url(self, poet_keys):
        """Tests an API call to get a Poet's details using its url"""
        poet_instance = Poet.find_by_url(url="/hafez")
        assert isinstance(poet_instance, Poet)
        assert poet_instance.full_url == '/hafez', "The url should be in the response"
        assert set(poet_keys).issubset(poet_instance.__dict__.keys()
                                       ), "All keys should be in the response"

    @vcr.use_cassette('tests/vcr_cassettes/poets_all.yml')
    def test_poet_all(self, poet_keys):
        poets = Poet.all()
        assert isinstance(poets, list)
        for poet in poets:
            assert set(poet_keys).issubset(
                poet.__dict__.keys()), "All keys should be in poet_instance"
