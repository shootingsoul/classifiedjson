# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from typing import Any
from classifiedjson.constants import CUSTOM_ATTRIBUTE_SERIALIZE, CUSTOM_ATTRIBUTE_DESERIALIZE
from classifiedjson.factory import Factory
from classifiedjson.utils import get_type_name


def serialize_custom_attribute(obj: Any) -> Any:
    serialize = getattr(obj, CUSTOM_ATTRIBUTE_SERIALIZE, None)
    if not serialize:
        # skip any objects that don't have the custom serialize attribute
        return NotImplemented

    try:
        custom_serialized = serialize()
        return custom_serialized
    except Exception as exc:
        raise RuntimeError(
            f"Error calling custom serialization {get_type_name(type(obj))}.{CUSTOM_ATTRIBUTE_SERIALIZE}") from exc


def deserialize_custom_attribute(factory: Factory, obj: Any):
    deserialize = getattr(factory._get_cls(),
                          CUSTOM_ATTRIBUTE_DESERIALIZE, None)
    if deserialize:
        try:
            return deserialize(factory, obj)
        except Exception as exc:
            raise RuntimeError(
                f"Error calling custom deserialization {factory}.{CUSTOM_ATTRIBUTE_DESERIALIZE}") from exc
    else:
        # need to raise error here because obj was serialized by a custom attribute
        # so this is the only thing that can deserialize it
        raise TypeError(
            f"Missing custom deserialization function {factory}.{CUSTOM_ATTRIBUTE_DESERIALIZE}.")
