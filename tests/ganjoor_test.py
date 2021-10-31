# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from pytest import fixture, mark
import pytest
from ganjoor import Ganjoor, GanjoorException
from dotenv import load_dotenv
from os import environ
import vcr

from ganjoor.models import Category, Poem, Poet


class TestGanjoor:

    @fixture()
    def ganjoor(self):
        return Ganjoor()

    @fixture
    def ganjoor_keys(self):
        return ['token', 'language', 'app_name', 'base_url']

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
                '_plain_text', '_html_text', '_ganjoor_metre']

    def test_init(self, ganjoor_keys, ganjoor):
        assert isinstance(ganjoor, Ganjoor)
        assert set(ganjoor_keys).issubset(ganjoor.__dict__.keys())

    @vcr.use_cassette('tests/vcr_cassettes/ganjoor_login.yml')
    def test_log_in(self, ganjoor):
        load_dotenv()
        username = environ.get('USERNAME')
        password = environ.get('PASSWORD')
        if username == '' or password == '':
            with pytest.raises(GanjoorException):
                ganjoor.log_in(username=username, password=password)

        else:
            ganjoor.log_in(username=username, password=password)
            assert ganjoor.auth_token

# Poet Tests
    @vcr.use_cassette('tests/vcr_cassettes/ganjoor_find_poet_id.yml')
    def test_find_poet_by_id(self, ganjoor):
        poet = ganjoor.find_poet_by_id(2)
        assert isinstance(poet, Poet)
        assert poet.id == 2

    @vcr.use_cassette('tests/vcr_cassettes/ganjoor_find_poet_url.yml')
    def test_find_poet_by_url(self, ganjoor):
        poet = ganjoor.find_poet_by_url('/hafez')
        assert isinstance(poet, Poet)
        assert poet.full_url == '/hafez'

    @vcr.use_cassette('tests/vcr_cassettes/ganjoor_get_all_poets.yml')
    def test_get_all_poets(self, ganjoor):
        poets = ganjoor.get_all_poets()
        assert [isinstance(poet, Poet) for poet in poets]

# Category Tests
    @mark.parametrize("vcr_cassette, with_poems", [
        ('tests/vcr_cassettes/ganjoor_find_category_by_id_with_poems.yml', True),
        ('tests/vcr_cassettes/ganjoor_find_category_by_id_without_poems.yml', False)])
    def test_find_category_by_id(self, vcr_cassette: str, with_poems, ganjoor):
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
    def test_find_category_by_url(self, vcr_cassette, with_poems, ganjoor):
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

    @mark.parametrize("id,vcr_cassette, complete", [
        (2131, 'tests/vcr_cassettes/ganjoor_find_poem_by_id_complete.yml', True),
        (2131, 'tests/vcr_cassettes/ganjoor_find_poem_by_id_incomplete.yml', False)
    ])
    def test_ganjoor_find_poem_by_id(self, id, vcr_cassette, complete,
                                     poem_keys_complete, poem_keys_incomplete, ganjoor):
        with vcr.use_cassette(vcr_cassette):
            poem = ganjoor.find_poem_by_id(id, complete=complete)
            assert isinstance(poem, Poem)
            assert poem.id == id
            if complete:
                for attr in poem_keys_complete:
                    assert (getattr(poem, attr, []))

            else:
                for attr in poem_keys_incomplete:
                    assert (getattr(poem, attr, []))

    @mark.parametrize("url,vcr_cassette, complete", [
        ('/hafez/ghazal/sh2',
         'tests/vcr_cassettes/ganjoor_find_poem_by_url_complete.yml', True),
        ('/hafez/ghazal/sh2',
         'tests/vcr_cassettes/ganjoor_find_poem_by_url_incomplete.yml', False)
    ])
    def test_ganjoor_find_poem_by_url(self, url, vcr_cassette, complete,
                                      poem_keys_complete, poem_keys_incomplete, ganjoor):
        with vcr.use_cassette(vcr_cassette):
            poem = ganjoor.find_poem_by_url(url, complete=complete)
            assert isinstance(poem, Poem)
            assert poem.full_url == url
            if complete:
                for attr in poem_keys_complete:
                    assert (getattr(poem, attr, []))

            else:
                for attr in poem_keys_incomplete:
                    assert (getattr(poem, attr, []))

    @vcr.use_cassette('tests/vcr_cassettes/ganjoor_hafez_faal.yml')
    def test_ganjoor_hafez_faal(self, poem_keys_incomplete, ganjoor):
        faal = ganjoor.hafez_faal()
        assert isinstance(faal, Poem)
        for attr in poem_keys_incomplete:
            assert (getattr(faal, attr, []))
        assert faal.get_poet_name_from_url() == "hafez"

    @mark.parametrize("poet_id,vcr_cassette", [
                      (0, 'tests/vcr_cassettes/ganjoor_random_poem.yml'),
                      (2, 'tests/vcr_cassettes/ganjoor_random_poem_by_hafez.yml')
                      ])
    def test_ganjoor_random_poem(self, poem_keys_incomplete, poet_id,
                                 vcr_cassette, ganjoor):
        with vcr.use_cassette(vcr_cassette):
            poem = ganjoor.random_poem(poet_id)
        assert isinstance(poem, Poem)
        if poet_id == 2:
            assert poem.get_poet_name_from_url() == "hafez"
        for attr in poem_keys_incomplete:
            assert getattr(poem, attr, [])

    @mark.parametrize("metre,rhyme,vcr_cassette", [
                      ('مفعول مفاعلن فعولن (هزج مسدس اخرب مقبوض محذوف)',
                       'ست',
                       'tests/vcr_cassettes/ganjoor_similar_poem_w_rhyme.yml'),
                      ('فعولن فعولن فعولن فعل (متقارب مثمن محذوف یا وزن شاهنامه)',
                       None,
                       'tests/vcr_cassettes/ganjoor_similar_poem_wo_rhyme.yml')
                      ])
    def test_ganjoor_find_similar_poems(self, poem_keys_incomplete, metre,
                                        rhyme, vcr_cassette, ganjoor):
        with vcr.use_cassette(vcr_cassette):
            similar_poems = ganjoor.find_similar_poems(
                metre=metre, rhyme=rhyme)
        assert len(similar_poems) == 5
        for poem in similar_poems:
            assert poem.ganjoor_metre.rhythm == metre
            if rhyme:
                assert poem.rhyme_letters == rhyme
            for attr in poem_keys_incomplete:
                assert getattr(poem, attr, [])

    @mark.parametrize("term,poet_id,cat_id,vcr_cassette", [
                      ('شیراز',
                       0,
                       0,
                       'tests/vcr_cassettes/ganjoor_search_poems_wo_cat.yml'),
                      ('شیراز',
                       2,
                       24,
                       'tests/vcr_cassettes/ganjoor_search_poems_w_cat.yml')
                      ])
    def test_ganjoor_search_poems(self, poem_keys_incomplete, term, poet_id, cat_id, ganjoor: Ganjoor, vcr_cassette):
        with vcr.use_cassette(vcr_cassette):
            poems = ganjoor.search_poems(term, poet_id=poet_id, cat_id=cat_id)
        assert len(poems) == 5
        for poem in poems:
            assert term in str(poem)
            if poet_id == 2 and cat_id == 24:
                assert poem.poet.id == poet_id
                assert (poem.category == cat_id) or (
                    cat_id in [child.id for child in poem.category.children])
            for attr in poem_keys_incomplete:
                assert getattr(poem, attr, [])
