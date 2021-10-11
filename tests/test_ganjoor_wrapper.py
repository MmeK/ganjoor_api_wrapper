# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT


from pytest import fixture


@fixture
def poem_keys():
    return ['id', 'title', 'fullTitle', 'urlSlug', 'fullUrl', 'plainText',
            'htmlText', 'ganjoorMetre', 'rhymeLetters', 'sourceName',
            'sourceUrlSlug', 'oldTag', 'oldTagPageUrl', 'category',
            'next', 'previous', 'verses', 'recitations', 'images', 'songs',
            'comments']

    # def test_poem_info(poem_keys):
    #     """Tests an API call to get a Poem's info"""
    #     poem_instance = Poem(1137)
    #     response = poem_instance.info()
    #     assert isinstance(response, dict)
    #     assert response['id'] == 1137, "The ID should be in the response"
    #     assert set(poem_keys).issubset(response.keys()
    #                                    ), "All keys should be in the response"
