# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from classifiedjson import dumps, loads
from typing import ClassVar, TypeVar
from tests.utils import dumps_and_loads
from logging import getLogger

logger = getLogger(__name__)


@dataclass
class MyConfigDC:
    data: list[str] = field(default_factory=lambda: ["en", "de"])
    min: int = 34
    max: int = 60


@dataclass
class MyConfigClassVar:
    min: int = 34
    max: int = 60
    pi: ClassVar[float] = 3.14

def test_plain():
    c = MyConfigDC()
    d = dumps_and_loads(c)
    assert type(d) == MyConfigDC
    assert c == d


def test_mod():
    c = MyConfigDC()
    c.data[0] = 'fr'
    c.max = 99
    d = dumps_and_loads(c)
    assert type(d) == MyConfigDC
    assert c == d


def test_class_var():
    # class var should be ignored automatically
    c = MyConfigClassVar()
    c.min = 0
    c.max = 99
    # serialize when pi = 3.14
    s = dumps(c)
    # now change the class var
    MyConfigClassVar.pi = 1000
    d = loads(s)
    # make sure pi is still incorrect and not touched by deserialization of instance
    assert d.pi == 1000
    assert d.min == 0
    assert d.max == 99



# T = TypeVar('T')

# @dataclass
# class MyGeneric(Generic[T]):
#     foo: T

# MyGenericStr = MyGeneric[str]

# def test_generic():
#     #FUTURE: support generics or determine if generic to raise error
#     # c = MyGenericStr("bar")
#     # d = dumps_and_loads(c)
#     # assert type(d) == MyGenericStr
#     # assert d.foo == "bar"
#     pass
