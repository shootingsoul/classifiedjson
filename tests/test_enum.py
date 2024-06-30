# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from enum import Enum, IntEnum
from tests.utils import dumps_and_loads
from logging import getLogger

logger = getLogger(__name__)


class MyState(Enum):
    IDLE = 1
    STARTING = 2
    RUNNING = 3
    STOPPED = 4


class Binary(Enum):
    A = True
    B = False


class MyIntEnum(IntEnum):
    RED = 0
    YELLOW = 1
    GREEN = 2


def test_enum():
    c = {"old_state": MyState.STARTING, "current_state": MyState.RUNNING}
    d = dumps_and_loads(c)
    assert type(d["old_state"]) == MyState
    assert c == d


def test_binary():
    # edge case, bool of false may serialize to a skip/ignore.
    # Make sure False is serialized
    c = {"old_state": Binary.A, "current_state": Binary.B}
    d = dumps_and_loads(c)
    assert type(d["old_state"]) == Binary
    assert c == d


def test_int():
    c = {"light": MyIntEnum.YELLOW}
    d = dumps_and_loads(c)
    assert type(d["light"]) == MyIntEnum
    assert c == d
