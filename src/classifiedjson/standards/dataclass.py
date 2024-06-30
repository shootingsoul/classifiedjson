# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from dataclasses import is_dataclass
from typing import Any
from classifiedjson.factory import Factory
from logging import getLogger


logger = getLogger(__name__)


def serialize_dataclass(obj: Any) -> Any:
    if not is_dataclass(type(obj)):
        return NotImplemented

    logger.debug("serialize dataclass start")
    d = {}
    # NOTE: ClassVar only included if instance overrides the class value
    #      This is the behavior we want, we don't want to have side-effects and change class values
    #      and we don't want to include any class values in serialization
    fields = vars(obj).items()
    for field_name, field_value in fields:
        # ignore dunders
        if not field_name.startswith('__'):
            d[field_name] = field_value

    return d


def deserialize_dataclass(factory: Factory, obj: Any) -> Any:
    cls = factory._get_cls()
    if not is_dataclass(cls):
        raise TypeError(
            f"Wrong type.  Expected type dataclass but received '{factory}' for deserializaiton")

    if not isinstance(obj, dict):
        raise ValueError(
            f"Dataclass deserailization requires a dict.  Received '{factory}'")

    return factory(**obj)
