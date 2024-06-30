# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from logging import getLogger
from dataclasses import dataclass
from tests.utils import dumps_and_loads
from classifiedjson import Factory

logger = getLogger(__name__)


class CustomScalar:
    def __init__(self, x: int) -> None:
        self.x = x

    def classifiedjson_serialize(self):
        return self.x

    @classmethod
    def classifiedjson_deserialize(cls, factory: Factory, obj):
        return factory(obj)


class CustomInherited(CustomScalar):
    def __init__(self, x: int) -> None:
        super().__init__(x)

    def what_is_my_value(self):
        return self.x


@dataclass
class CustomDataclass:
    x: int = 7
    pi: float = 3.14
    z: str = "hello"

    def classifiedjson_serialize(self):
        return {'x': self.x, 'z': self.z}

    @classmethod
    def classifiedjson_deserialize(cls, factory: Factory, obj):
        return CustomDataclass(**obj)


# FUTURE  generic custom dataclass


def test_class_scalar_none():
    a = CustomScalar(None)
    d = dumps_and_loads(a)
    assert d.x is None


def test_class_scalar():
    a = CustomScalar(5)
    d = dumps_and_loads(a)
    assert a.x == d.x


def test_dataclass():
    # also ensures we can customize dc behavior
    data = CustomDataclass()
    data.pi = 99  # should skip serialization of this field
    data.z = "hello world"
    d = dumps_and_loads(data)
    assert d.x == 7
    assert d.pi == 3.14
    assert d.z == "hello world"


def test_inherit():
    # make sure base custom serialization is used
    # but that we get the same type back
    a = CustomInherited(99)
    d = dumps_and_loads(a)
    assert d.what_is_my_value() == 99
