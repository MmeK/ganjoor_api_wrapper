# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from pytest import fixture, mark
from ganjoor import Ganjoor
from dotenv import load_dotenv
from os import environ
import vcr

from ganjoor.models import Category, Poet


class TestGanjoor:
    @fixture
    def ganjoor_keys(self):
        return ['token', 'language', 'app_name', 'base_url']

    def test_init(self, ganjoor_keys):
        ganjoor = Ganjoor()
        assert isinstance(ganjoor, Ganjoor)
        assert set(ganjoor_keys).issubset(ganjoor.__dict__.keys())

    @vcr.use_cassette('tests/vcr_cassettes/ganjoor_login.yml')
    def test_log_in(self):
        load_dotenv()
        username = environ.get('USERNAME')
        password = environ.get('PASSWORD')
        ganjoor = Ganjoor()
        ganjoor.log_in(username=username, password=password)
        assert ganjoor.auth_token

# Poet Tests
    @vcr.use_cassette('tests/vcr_cassettes/ganjoor_find_poet_id.yml')
    def test_find_poet_by_id(self):
        ganjoor = Ganjoor()
        poet = ganjoor.find_poet_by_id(2)
        assert isinstance(poet, Poet)
        assert poet.id == 2

    @vcr.use_cassette('tests/vcr_cassettes/ganjoor_find_poet_url.yml')
    def test_find_poet_by_url(self):
        ganjoor = Ganjoor()
        poet = ganjoor.find_poet_by_url('/hafez')
        assert isinstance(poet, Poet)
        assert poet.full_url == '/hafez'

    @vcr.use_cassette('tests/vcr_cassettes/ganjoor_get_all_poets.yml')
    def test_get_all_poets(self):
        ganjoor = Ganjoor()
        poets = ganjoor.get_all_poets()
        assert [isinstance(poet, Poet) for poet in poets]

# Category Tests
    @mark.parametrize("vcr_cassette, with_poems", [
        ('tests/vcr_cassettes/ganjoor_find_category_by_id_with_poems.yml', True),
        ('tests/vcr_cassettes/ganjoor_find_category_by_id_without_poems.yml', False)])
    def test_find_category_by_id(self, vcr_cassette: str, with_poems):
        ganjoor = Ganjoor()
        with vcr.use_cassette(vcr_cassette):
            category = ganjoor.find_category_by_id(24, with_poems)
        assert isinstance(category, Category)
        assert category.id == 24
        assert isinstance(category.poems, list)
        if with_poems:
            assert len(category.poems) > 0
        else:
            assert len(category.poems) == 0

    @mark.parametrize("vcr_cassette, with_poems", [
        ('tests/vcr_cassettes/ganjoor_find_category_by_url_with_poems.yml', True),
        ('tests/vcr_cassettes/ganjoor_find_category_by_url_without_poems.yml', False)])
    def test_find_category_by_url(self, vcr_cassette, with_poems):
        ganjoor = Ganjoor()
        with vcr.use_cassette(vcr_cassette):
            category = ganjoor.find_category_by_url(
                '/hafez/ghazal', with_poems)
        assert isinstance(category, Category)
        assert category.full_url == '/hafez/ghazal'
        assert isinstance(category.poems, list)
        if with_poems:
            assert len(category.poems) > 0
        # else:
        #     assert len(category.poems) == 0 TODO: API Problem

# Poem Tests
