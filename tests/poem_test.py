# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from pytest import fixture
from ganjoor import Poem
import vcr

from ganjoor.poem_utils import Comment, IncompletePoem, Metre, PoemImage, Recitation, Song, Verse

TEST_POEM_ID = 2131


class TestPoem:
    """Poem Test Class"""

    @fixture
    def poem_string(self):
        return """صلاح کار کجا و من خراب کجا"""

    @fixture
    def poem(self):
        with vcr.use_cassette('tests/vcr_cassettes/poem_find_complete.yml'):
            return Poem.find(TEST_POEM_ID, complete=True)

    @fixture
    def poem_keys_complete(self):
        return ['_id', '_title', '_full_title', '_url_slug', '_full_url',
                '_plain_text', '_html_text', '_ganjoor_metre',
                '_rhyme_letters', '_source_name', '_source_url_slug',
                '_category', '_next',
                '_previous', '_verses', '_recitations', '_images', '_songs',
                '_comments']

    @fixture
    def poem_keys_incomplete(self):
        return ['_id', '_title', '_full_title', '_url_slug', '_full_url',
                '_plain_text', '_html_text', '_ganjoor_metre',
                '_rhyme_letters', '_source_name', '_source_url_slug']

    @vcr.use_cassette('tests/vcr_cassettes/poem_find.yml')
    def test_poem_find(self, poem_keys_complete):
        """Tests API call to find a poem by its Id"""
        poem_instance = Poem.find(2130)
        assert isinstance(poem_instance, Poem)
        assert poem_instance.id == 2130, "The ID should be in the poem_instance"
        assert set(poem_keys_complete).issubset(poem_instance.__dict__.keys()
                                                ), "All keys should be in the response"

    @vcr.use_cassette('tests/vcr_cassettes/poem_find_by_url.yml')
    def test_poem_find_by_url(self, poem_keys_complete):
        """Tests API call to find a poem by its Url"""
        poem_instance = Poem.find_by_url("/hafez/ghazal/sh2")
        assert isinstance(poem_instance, Poem)
        assert poem_instance.full_url == "/hafez/ghazal/sh2", "The url should be in the poem_instance"
        assert set(poem_keys_complete).issubset(poem_instance.__dict__.keys()
                                                ), "All keys should be in the response"

    @vcr.use_cassette('tests/vcr_cassettes/poem_random.yml')
    def test_poem_random(self, poem_keys_complete):
        """Tests API call to get a random Poem"""
        poem_instance = Poem.random()
        assert isinstance(poem_instance, Poem)
        assert set(poem_keys_complete).issubset(poem_instance.__dict__.keys()
                                                ), "All keys should be in the response"

    @vcr.use_cassette('tests/vcr_cassettes/poem_random_saadi.yml')
    def test_poem_random_from_saadi(self, poem_keys_complete):
        """Tests API call to get a random Poem from saadi"""
        poem_instance = Poem.random(poet_id=7)
        assert isinstance(poem_instance, Poem)
        assert poem_instance.full_url.split(
            '/')[1] == "saadi", "The ID should be correct"
        assert set(poem_keys_complete).issubset(poem_instance.__dict__.keys()
                                                ), "All keys should be in the response"

    @vcr.use_cassette('tests/vcr_cassettes/poem_similar.yml')
    def test_poem_similar(self, poem_keys_complete):
        """Tests Api call to get similar Poems"""
        poem_list = Poem.similar()
        for poem in poem_list:
            assert isinstance(poem, Poem)
            set(poem_keys_complete).issubset(poem.__dict__.keys())
            "All keys should be in the response"

    @vcr.use_cassette('tests/vcr_cassettes/poem_search.yml')
    def test_poem_search(self, poem_keys_complete):
        """Tests Api call to search for a term in all poems"""
        poem_list = Poem.search(term="شیراز")
        for poem in poem_list:
            assert isinstance(poem, Poem)
            assert set(poem_keys_complete).issubset(poem.__dict__.keys()),\
                "All keys should be in the response"

    @vcr.use_cassette('tests/vcr_cassettes/poem_request_recitations.yml')
    def test_request_recitations(self, poem: Poem):
        for recitation in poem.request_recitations():
            assert isinstance(recitation, Recitation)

    @vcr.use_cassette('tests/vcr_cassettes/poem_request_images.yml')
    def test_request_images(self, poem: Poem):
        for image in poem.request_images():
            assert isinstance(image, PoemImage)

    @vcr.use_cassette('tests/vcr_cassettes/poem_request_songs.yml')
    def test_request_songs(self, poem: Poem):
        for song in poem.request_songs():
            assert isinstance(song, Song)

    @vcr.use_cassette('tests/vcr_cassettes/poem_request_comments.yml')
    def test_request_comments(self, poem: Poem):
        for comment in poem.request_comments():
            assert isinstance(comment, Comment)

    @vcr.use_cassette('tests/vcr_cassettes/poem_hafez_faal.yml')
    def test_hafez_faal(self):
        """Tests an API call to get a faal from Hafez"""
        faal = Poem.hafez_faal()
        assert faal
        assert isinstance(faal, Poem)
        assert faal.get_poet_name_from_url() == 'hafez'

    def test_poem_str(self, poem: Poem, poem_string):
        assert str(poem.get_all_couplets()[0].verses[0]) == poem_string

    def test_ganjoor_metre(self, poem: Poem):
        assert isinstance(poem.ganjoor_metre, Metre)

    def test_category(self, poem: Poem):
        assert isinstance(poem.ganjoor_metre, Metre)

    def test_poet(self, poem: Poem):
        assert isinstance(poem.ganjoor_metre, Metre)

    def test_recitations(self, poem: Poem):
        assert poem.recitations
        for recitation in poem.recitations:
            assert isinstance(recitation, Recitation)

    def test_songs(self, poem: Poem):
        assert poem.songs
        for song in poem.songs:
            assert isinstance(song, Song)

    def test_comments(self, poem: Poem):
        assert poem.comments
        for comment in poem.comments:
            assert isinstance(comment, Comment)

    def test_images(self, poem: Poem):
        for image in poem.images:
            assert isinstance(image, PoemImage)

    def test_previous_poem(self, poem: Poem):
        assert isinstance(poem.previous_poem, IncompletePoem)

    def test_next_poem(self, poem: Poem):
        assert isinstance(poem.next_poem, IncompletePoem)

    def test_normal_image_urls(self, poem):
        for poem_image in poem.images:
            assert isinstance(poem_image.normal_image_url, str)

    def test_thumbnail_urls(self, poem: Poem):
        for poem_image in poem.images:
            assert isinstance(poem_image.thumbnail_image_url, str)

    def test_verses(self, poem: Poem):
        for verse in poem.verses:
            assert isinstance(verse, Verse)

    def test_id(self, poem: Poem):
        assert isinstance(poem.id, int)

    def test_title(self, poem: Poem):
        assert isinstance(poem.title, str)

    def test_full_title(self, poem: Poem):
        assert isinstance(poem.full_title, str)

    def test_url_slug(self, poem: Poem):
        assert isinstance(poem.url_slug, str)

    def test_full_url(self, poem: Poem):
        assert isinstance(poem.full_url, str)

    def test_plain_text(self, poem: Poem):
        assert isinstance(poem.plain_text, str)

    def test_html_text(self, poem: Poem):
        assert isinstance(poem.html_text, str)

    def test_rhyme_letters(self, poem: Poem):
        assert isinstance(poem.rhyme_letters, str)

    def test_source_name(self, poem: Poem):
        assert isinstance(poem.source_name, str)

    def test_source_url_slug(self, poem: Poem):
        assert isinstance(poem.source_url_slug, str)

    def test_old_tag(self, poem: Poem):
        assert isinstance(poem.old_tag, type(None))

    def test_old_tag_page_url(self, poem: Poem):
        assert isinstance(poem.old_tag_page_url, type(None))
