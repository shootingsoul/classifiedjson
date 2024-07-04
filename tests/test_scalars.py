# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

import uuid
from decimal import Decimal
from uuid import UUID
from logging import getLogger
from tests.utils import dumps_and_loads


logger = getLogger(__name__)


class Mystr(str):
    pass


class Myint(int):
    pass


class Myfloat(float):
    pass


class MyDecimal(Decimal):
    pass

class MyUUID(UUID):
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

def test_decimal():
    v = Decimal("3.14")
    d = dumps_and_loads(v)
    assert type(d) == Decimal
    assert v == d

    v = Decimal("nan")
    d = dumps_and_loads(v)
    assert type(d) == Decimal
    assert d.is_nan() == True

    v = Decimal("-inf")
    d = dumps_and_loads(v)
    assert type(d) == Decimal
    assert d.is_infinite() == True
    assert d < 0

    v = Decimal("inf")
    d = dumps_and_loads(v)
    assert type(d) == Decimal
    assert d.is_infinite() == True
    assert d > 0

    v = Decimal("1.045753453457657657")
    d = dumps_and_loads(v)
    assert type(d) == Decimal
    assert v == d


def test_decimal_subclass():
    v = MyDecimal("12343134123.1231409814")
    d = dumps_and_loads(v)
    assert type(d) == MyDecimal
    assert v == d


def test_uuid():
    v = uuid.uuid1()
    d = dumps_and_loads(v)
    assert type(d) == UUID
    assert v == d
    assert v.version == d.version

    v = uuid.uuid3(uuid.NAMESPACE_DNS, 'shootingsoul.com')
    d = dumps_and_loads(v)
    assert type(d) == UUID
    assert v == d
    assert v.version == d.version

    v = uuid.uuid4()
    d = dumps_and_loads(v)
    assert type(d) == UUID
    assert v == d
    assert v.version == d.version

    v = uuid.uuid5(uuid.NAMESPACE_DNS, 'shootingsoul.com')
    d = dumps_and_loads(v)
    assert type(d) == UUID
    assert v == d
    assert v.version == d.version


def test_uuid_subclass():
    u = uuid.uuid4()
    v = MyUUID(str(u))
    d = dumps_and_loads(v)
    assert type(d) == MyUUID
    assert v == d
