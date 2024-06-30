# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from logging import getLogger
from tests.utils import dumps_and_loads


logger = getLogger(__name__)


class Mystr(str):
    pass


class Myint(int):
    pass


class Myfloat(float):
    pass


def test_mystr():
    m = Mystr("abc")
    d = dumps_and_loads(m)
    assert type(d) == Mystr
    assert m == d

    m = Mystr(None)
    d = dumps_and_loads(m)
    assert type(d) == Mystr
    assert m == d


def test_myint():
    m = Myint(99)
    d = dumps_and_loads(m)
    assert type(d) == Myint
    assert m == d


def test_myfloat():
    m = Myfloat(3.14)
    d = dumps_and_loads(m)
    assert type(d) == Myfloat
    assert m == d
