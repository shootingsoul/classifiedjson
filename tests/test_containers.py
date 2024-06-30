# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from logging import getLogger
from tests.utils import dumps_and_loads


logger = getLogger(__name__)


class ListSub(list):

    def sum(self):
        s = 0
        for i in self:
            s += i
        return s


class DictSub(dict):

    def get_sum_lasts(self):
        sum = 0
        for k, value in self.items():
            sum += value[-1]
        return sum


def test_list_sub():
    l = ListSub(range(11, 17))
    sum = l.sum()

    l2 = dumps_and_loads(l)
    sum2 = l2.sum()

    assert l == l2
    assert sum == sum2


def test_list_sub_empty():
    l = ListSub()
    l2 = dumps_and_loads(l)
    assert type(l2) == ListSub
    assert len(l2) == 0


def test_dict_sub():
    d = DictSub()
    d['a'] = list(range(11, 17))
    d['b'] = list(range(100, 124))
    sum = d.get_sum_lasts()

    d2 = dumps_and_loads(d)
    sum2 = d2.get_sum_lasts()

    assert d == d2
    assert sum == sum2


def test_dict_sub_empty():
    d = DictSub()
    d2 = dumps_and_loads(d)
    assert type(d2) == DictSub
    assert len(d2) == 0


def test_tuple():
    t = ("LA", 1, 2)
    t2 = dumps_and_loads(t)
    assert type(t2) == tuple
    assert t == t2


def test_set():
    cities = {"LA", "NY", "MIAMI"}
    s = dumps_and_loads(cities)
    assert type(s) == set
    assert s == cities

    empty = set()
    s = dumps_and_loads(empty)
    assert type(s) == set
    assert len(s) == 0


def test_frozen_set():
    cities = frozenset(["LA", "NY", "MIAMI"])
    s = dumps_and_loads(cities)
    assert type(s) == frozenset
    assert s == cities

    empty = frozenset()
    s = dumps_and_loads(empty)
    assert type(s) == frozenset
    assert len(s) == 0
