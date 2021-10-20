# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT

from pytest import fixture
from ganjoor import Category
import vcr


class TestCategory:
    @fixture
    def category_keys(self):
        return ['_id', '_title', '_url_slug', '_full_url', '_next',
                '_previous', '_ancestors', '_children', '_poems']

    @vcr.use_cassette('tests/vcr_cassettes/category_find.yml')
    def test_category_find(self, category_keys):
        """Tests an API call for finding a Category by its Id using Category.find()"""
        category_instance = Category.find(24)
        assert isinstance(category_instance, Category)
        assert category_instance.id == 24, "The Id should be correct"
        assert set(category_keys).issubset(
            category_instance.__dict__.keys()), "All keys should be in response"

    @vcr.use_cassette('tests/vcr_cassettes/category_find_by_url.yml')
    def test_category_find_by_url(self, category_keys):
        """Tests an API call for finding a Category by its Id using Category.find()"""
        category_instance = Category.find_by_url("/hafez")
        assert isinstance(category_instance, Category)
        assert category_instance.full_url == "/hafez", "The Id should be correct"
        assert set(category_keys).issubset(
            category_instance.__dict__.keys()), "All keys should be in response"
