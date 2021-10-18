# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT

from __future__ import annotations
from dataclasses import dataclass
from typing import List
from inflection import underscore


class Metre:
    def __init__(self, metre_args) -> None:
        for key in metre_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, metre_args[key])

    @property
    def id(self) -> int:
        return self._id

    @property
    def url_slug(self) -> str:
        return self._url_slug

    @property
    def rhythm(self) -> str:
        return self._rhythm

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def verse_count(self) -> int:
        return self._verse_count


class PoemImage:
    def __init__(self, poem_image_args) -> None:
        for key in poem_image_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, poem_image_args[key])

    @property
    def normal_image_url(self) -> str:
        return self.thumbnail_image_url.replace('thumb', 'normal')

    @property
    def image_order(self) -> int:
        return self._image_order

    @property
    def poem_related_image_type(self) -> int:
        return self._poem_related_image_type

    @property
    def thumbnail_image_url(self) -> str:
        return self._thumbnail_image_url

    @property
    def target_page_url(self) -> str:
        return self._target_page_url

    @property
    def alt_text(self) -> str:
        return self._alt_text


@dataclass
class Verse:
    _id: int
    _v_order: int
    _couplet_index: int
    _verse_position: int
    _text: str

    def __init__(self, verse_args):
        for key in verse_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, verse_args[key])

    @property
    def id(self) -> int:
        return self._id

    @property
    def v_order(self) -> int:
        return self._v_order

    @property
    def couplet_index(self) -> int:
        return self._couplet_index

    @property
    def verse_position(self) -> int:
        return self._verse_position

    @property
    def text(self) -> str:
        return self._text


@dataclass
class Couplet:
    _verses: List[Verse]

    @property
    def verses(self) -> List[Verse]:
        return self._verses

    def __str__(self):
        return '\n'.join([verse.text for verse in self.verses])


@dataclass
class Song:
    _id: int
    _poem_id: int
    _track_type: int
    _artist_name: str
    _artist_url: str
    _album_name: str
    _album_url: str
    _track_name: str
    _track_url: str
    _description: str
    _broken_link: bool
    _golha_track_id: int
    _approved: int
    _rejected: int
    _rejected_cause: str
    _suggested_by_id: str
    _suggested_by_nickname: str

    def __init__(self, song_args):
        for key in song_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, song_args[key])


@dataclass
class Comment:
    _id: int
    _author_name: str
    _author_url: str
    _comment_date: str
    _html_comment: str
    _publish_status: str
    _in_reply_to_id: int
    _user_id: int
    _replies: List[Comment]
    _my_comment: bool
    _couplet_index: int
    _couplet_summary: str

    def __init__(self, comment_args):
        for key in comment_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, comment_args[key])

    @property
    def replies(self):
        return [Comment(comment) for comment in self._replies]


@dataclass
class Recitation:
    _id: int
    _poem_id: int
    _poem_full_title: str
    _poem_full_url: str
    _audio_title: str
    _audio_artist: str
    _audio_artist_url: str
    _audio_src: str
    _audio_src_url: str
    _legacy_audio_guid: str
    _mp3_file_check_sum: str
    _mp3_size_in_bytes: int
    _publish_date: str
    _file_last_updated: str
    _mp3_url: str
    _xml_text: str
    _plain_text: str
    _html_text: str

    def __init__(self, recitation_args):
        for key in recitation_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, recitation_args[key])
