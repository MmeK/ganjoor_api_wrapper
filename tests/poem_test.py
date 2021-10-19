# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from pytest import fixture
from ganjoor import Poem
import vcr


class TestPoem:
    """Poem Test Class"""
    @fixture
    def poem_keys(self):
        return ['_id', '_title', '_full_title', '_url_slug', '_full_url',
                '_plain_text', '_html_text', '_ganjoor_metre',
                '_rhyme_letters', '_source_name', '_source_url_slug',
                '_old_tag', '_old_tag_page_url', '_category', '_next',
                '_previous', '_verses', '_recitations', '_images', '_songs',
                '_comments']

    @vcr.use_cassette('tests/vcr_cassettes/poem_find.yml')
    def test_poem_find(self, poem_keys):
        """Tests API call to find a poem by its Id"""
        poem_instance = Poem.find(2130)
        assert isinstance(poem_instance, Poem)
        assert poem_instance.id == 2130, "The ID should be in the poem_instance"
        assert set(poem_keys).issubset(poem_instance.__dict__.keys()
                                       ), "All keys should be in the response"

    @vcr.use_cassette('tests/vcr_cassettes/poem_find_by_url.yml')
    def test_poem_find_by_url(self, poem_keys):
        """Tests API call to find a poem by its Url"""
        poem_instance = Poem.find_by_url("/hafez/ghazal/sh2")
        assert isinstance(poem_instance, Poem)
        assert poem_instance.full_url == "/hafez/ghazal/sh2", "The url should be in the poem_instance"
        assert set(poem_keys).issubset(poem_instance.__dict__.keys()
                                       ), "All keys should be in the response"
