# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from typing import Any
from classifiedjson.factory import Factory
from classifiedjson.utils import is_match
from logging import getLogger
from enum import Enum


logger = getLogger(__name__)


def serialize_enum(obj: Any) -> Any:
    if not is_match(obj, Enum):
        return NotImplemented

    logger.debug("serialize enum")
    return obj.value


def deserialize_enum(factory: Factory, obj: Any) -> Any:
    if not factory.is_match(Enum):
        raise TypeError(
            f"Wrong type.  Expected type enum but received '{factory}' for deserializaiton")

    return factory(obj)
