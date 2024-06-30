# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from enum import Enum
from datetime import datetime, timedelta
from tests.utils import dumps_and_loads


class MyState(Enum):
    IDLE = 1
    STARTING = 2
    RUNNING = 3
    STOPPED = 4


def test_non_string_key():
    v = {}
    v[1] = "Chicago"
    v[2] = "New York"
    v[3] = "Miami"

    d = dumps_and_loads(v)
    keys = list(d.keys())
    assert isinstance(keys[2], int)
    assert v == d


def test_mix_key_types():
    v = {}
    v[1] = "Chicago"
    v["two"] = "New York"
    v[3] = "Miami"

    d = dumps_and_loads(v)
    keys = list(d.keys())
    assert isinstance(keys[1], str)
    assert isinstance(keys[2], int)
    assert v == d


def test_enum_key():

    v = {}
    v[MyState.STARTING] = {"city": "Chicago"}
    v[MyState.IDLE] = {"city": "NY"}
    v[MyState.RUNNING] = {"city": "Miami"}

    d = dumps_and_loads(v)
    keys = list(d.keys())
    assert isinstance(keys[1], MyState)
    assert v == d


def test_datetime_key():

    v = {}
    dt = datetime(2024, 1, 1, 5, 3, 2, 0)

    v[dt] = "Sunny"
    v[dt + timedelta(days=1)] = "Cloudy"
    v[dt + timedelta(days=2)] = "Rainy"

    d = dumps_and_loads(v)
    keys = list(d.keys())
    assert isinstance(keys[1], datetime)
    assert v == d


def test_special_key():

    v = {}
    v['square \u2588'] = "circle"

    d = dumps_and_loads(v)
    assert v == d
