# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from tests.utils import dumps_and_loads


def test_basic():
    # ensure types are preserved and numbers don't include commas
    # ensure float is preserved even with a zero fraction

    v = {"none": None,
         "int": 50000,
         "float": 6.0,
         "pi": 3.14159,
         "bool": False,
         "bool_again": True,
         "str": "hello"}
    d = dumps_and_loads(v)
    assert d["none"] is None
    assert type(d["int"]) == int
    assert type(d["float"]) == float
    assert type(d["pi"]) == float
    assert type(d["bool"]) == bool
    assert type(d["bool_again"]) == bool
    assert type(d["str"]) == str
    assert v == d


def test_encoding():
    v = {'hello': 'so-called "world" \u2588',
         '"foo"': '"bar"'
         }
    d = dumps_and_loads(v)
    assert v == d


def test_nested_dict():
    v = {'a': 1,
         "c": {"gamma": {"beta": {"delta": {"sigma": 4}}}},
         "b": {"x": 2, "y": 3},
         'd': 5
         }
    d = dumps_and_loads(v)
    assert v == d


def test_nested_list():
    v = {"a": [1, [[[[[4]], 2, 3]]]]}
    d = dumps_and_loads(v)
    assert v == d


def test_empty():
    v = {}
    d = dumps_and_loads(v)
    assert v == d

    v = {"a": []}
    d = dumps_and_loads(v)
    assert v == d
