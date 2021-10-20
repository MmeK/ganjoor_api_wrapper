# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT

from __future__ import annotations
from dataclasses import dataclass
from typing import List
from inflection import underscore


@dataclass
class Metre:
    _id: int
    _url_slug: str
    _rhythm: str
    _name: str
    _description: str
    _verse_count: int

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


@dataclass
class PoemImage:
    _image_order: int
    _poem_related_image_type: int
    _thumbnail_image_url: str
    _target_page_url: str
    _alt_text: str

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

    def __str__(self) -> str:
        return self.text


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

    @property
    def id(self) -> int:
        return self._id

    @property
    def poem_id(self) -> int:
        return self._poem_id

    @property
    def track_type(self) -> int:
        return self._track_type

    @property
    def artist_name(self) -> str:
        return self._artist_name

    @property
    def artist_url(self) -> str:
        return self._artist_url

    @property
    def album_name(self) -> str:
        return self._album_name

    @property
    def album_url(self) -> str:
        return self._album_url

    @property
    def track_name(self) -> str:
        return self._track_name

    @property
    def track_url(self) -> str:
        return self._track_url

    @property
    def description(self) -> str:
        return self._description

    @property
    def broken_link(self) -> bool:
        return self._broken_link

    @property
    def golha_track_id(self) -> int:
        return self._golha_track_id

    @property
    def approved(self) -> int:
        return self._approved

    @property
    def rejected(self) -> int:
        return self._rejected

    @property
    def rejected_cause(self) -> str:
        return self._rejected_cause

    @property
    def suggested_by_id(self) -> str:
        return self._suggested_by_id

    @property
    def suggested_by_nickname(self) -> str:
        return self._suggested_by_nickname


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

    # TODO: Add get recent comments

    @property
    def id(self) -> int:
        return self._id

    @property
    def replies(self) -> List[Comment]:
        return [Comment(comment) for comment in self._replies]

    @property
    def author_name(self) -> str:
        return self._author_name

    @property
    def author_url(self) -> str:
        return self._author_url

    @property
    def comment_date(self) -> str:
        return self._comment_date

    @property
    def html_comment(self) -> str:
        return self._html_comment

    @property
    def publish_status(self) -> str:
        return self._publish_status

    @property
    def in_reply_to_id(self) -> int:
        return self._in_reply_to_id

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def my_comment(self) -> bool:
        return self._my_comment

    @property
    def couplet_index(self) -> int:
        return self._couplet_index

    @property
    def couplet_summary(self) -> str:
        return self._couplet_summary


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

    @property
    def id(self) -> int:
        return self._id

    @property
    def poem_id(self) -> int:
        return self._poem_id

    @property
    def poem_full_title(self) -> str:
        return self._poem_full_title

    @property
    def poem_full_url(self) -> str:
        return self._poem_full_url

    @property
    def audio_title(self) -> str:
        return self._audio_title

    @property
    def audio_artist(self) -> str:
        return self._audio_artist

    @property
    def audio_artist_url(self) -> str:
        return self._audio_artist_url

    @property
    def audio_src(self) -> str:
        return self._audio_src

    @property
    def audio_src_url(self) -> str:
        return self._audio_src_url

    @property
    def legacy_audio_guid(self) -> str:
        return self._legacy_audio_guid

    @property
    def mp3_file_check_sum(self) -> str:
        return self._mp3_file_check_sum

    @property
    def mp3_size_in_bytes(self) -> int:
        return self._mp3_size_in_bytes

    @property
    def publish_date(self) -> str:
        return self._publish_date

    @property
    def file_last_updated(self) -> str:
        return self._file_last_updated

    @property
    def mp3_url(self) -> str:
        return self._mp3_url

    @property
    def xml_text(self) -> str:
        return self._xml_text

    @property
    def plain_text(self) -> str:
        return self._plain_text

    @property
    def html_text(self) -> str:
        return self._html_text


@dataclass
class IncompletePoem:
    _id: int
    _title: str
    _url_slug: str
    _excerpt: str
    _rhythm: str
    _rhyme_letters: str

    def __init__(self, incomplete_poem_args):
        for key in incomplete_poem_args.keys():
            snake_key = underscore(key)
            setattr(self, "_"+snake_key, incomplete_poem_args[key])

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def url_slug(self) -> str:
        return self._url_slug

    @property
    def excerpt(self) -> str:
        return self._excerpt

    @property
    def rhythm(self) -> str:
        return self._rhythm

    @property
    def rhyme_letters(self) -> str:
        return self._rhyme_letters
