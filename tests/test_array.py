# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from array import array

from logging import getLogger
from tests.utils import dumps_and_loads

logger = getLogger(__name__)


def test_zero_len():
    a = array('l', [])
    d = dumps_and_loads(a)
    assert a == d


def test_numeric():
    a = array('l', [1, 2, 3, 4, 5])
    d = dumps_and_loads(a)
    assert a == d


def test_string():
    a = array('u', 'hello \u2641')
    d = dumps_and_loads(a)
    assert a == d
