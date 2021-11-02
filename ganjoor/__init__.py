# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from .models import (Poet, Poem, Category)
from .ganjoor import Ganjoor
from .config import GANJGAH_BASE_URL
from .exceptions import GanjoorException
import requests_cache
from requests_cache import DO_NOT_CACHE

urls_expire_after = {
    GANJGAH_BASE_URL+Poem._urls['random']: DO_NOT_CACHE,
    GANJGAH_BASE_URL+Poem._urls['hafez_faal']: DO_NOT_CACHE,
    '*': -1
}


requests_cache.install_cache(
    cache_name='ganjoor_cache', backend='sqlite', urls_expire_after=urls_expire_after)
