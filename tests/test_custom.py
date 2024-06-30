# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

import pytest
from logging import getLogger
from classifiedjson import loads, dumps, Factory, is_exact_match
from datetime import datetime, timezone

logger = getLogger(__name__)

# custom is when we override / extend by pass into dump/load directly


class CustomScalar:
    def __init__(self, x: int) -> None:
        self.x = x


def my_serialize(obj):
    if not is_exact_match(obj, CustomScalar):
        return NotImplemented

    return obj.x


def my_deserialize(factory: Factory, obj):
    if not factory.is_match(CustomScalar):
        return NotImplemented

    return factory(obj)


def dt_serialize(obj):
    if not is_exact_match(obj, datetime):
        return NotImplemented

    # e.g. datetime serialize to force tz to utc
    timestamp = obj.replace(tzinfo=timezone.utc).timestamp()
    return timestamp


def dt_deserialize(factory: Factory, obj):
    if not factory.is_exact_match(datetime):
        return NotImplemented

    return datetime.fromtimestamp(obj, timezone.utc)


def test_extend():
    a = CustomScalar(5)
    s = dumps(a, my_serialize)
    d = loads(s, my_deserialize)
    assert a.x == d.x


def test_override():
    dt = datetime.now()
    dt_utc = dt.replace(tzinfo=timezone.utc)
    assert dt.timestamp() != dt_utc.timestamp()

    a = {'x': dt}
    s = dumps(a, dt_serialize)
    d = loads(s, dt_deserialize)

    assert d['x'].tzinfo == dt_utc.tzinfo
    assert d['x'].timestamp() == dt_utc.timestamp()


def test_multiple():
    a = CustomScalar(7)
    dt = datetime.now()

    m = {'a': a, 'dt': dt}
    s = dumps(m, [my_serialize, dt_serialize])
    d = loads(s, [my_deserialize, dt_deserialize])

    assert d['a'].x == a.x
    assert d['dt'].tzinfo == timezone.utc


def test_unsupported():
    a = CustomScalar(7)

    # forget to pass in serializer hook
    with pytest.raises(RuntimeError) as e_info:
        dumps(a)

    s = dumps(a, my_serialize)

    # forget to pass in deserializer hook
    with pytest.raises(RuntimeError) as e_info:
        loads(s)


##############################

class CustomList(list):
    pass


def cl_serialize(obj):
    if not is_exact_match(obj, CustomList):
        return NotImplemented
    # add 1
    # serialize as a normal list
    return [i + 1 for i in obj]


def cl_deserialize(factory: Factory, obj):
    if not factory.is_exact_match(CustomList):
        return NotImplemented
    # all good, pass it through
    return factory(obj)


def test_custom_list():
    # make sure we can override inherited standard containers or use the standard implementation
    l = CustomList([2, 2, 2, 2])

    s = dumps(l, cl_serialize)
    d = loads(s, cl_deserialize)

    assert type(d) == CustomList
    assert d == [3, 3, 3, 3]

    # use the standard serailization
    s = dumps(l)
    d = loads(s)

    assert type(d) == CustomList
    logger.debug(d)
    assert d == [2, 2, 2, 2]

##############################


class CustomDict(dict):
    pass


def cd_serialize(obj):
    if not is_exact_match(obj, CustomDict):
        return NotImplemented
    # add 1
    # serialize as a normal dict
    d = {}
    for key, value in obj.items():
        d[key] = value + 1
    return d


def cd_deserialize(factory: Factory, obj):
    if not factory.is_exact_match(CustomDict):
        return NotImplemented
    # all good, pass it through
    return factory(obj)


def test_custom_dict():
    # make sure we can override inherited standard containers or use the standard implementation
    cd = CustomDict()
    cd['a'] = 2
    cd['b'] = 4
    cd['c'] = 6

    s = dumps(cd, cd_serialize)
    d = loads(s, cd_deserialize)

    assert type(d) == CustomDict
    assert d['a'] == 3
    assert d['b'] == 5
    assert d['c'] == 7

    # use the standard serailization
    s = dumps(cd)
    d = loads(s)

    assert type(d) == CustomDict
    assert d['a'] == 2
    assert d['b'] == 4
    assert d['c'] == 6
