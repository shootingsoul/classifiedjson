# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from classifiedjson.factory import Factory
from typing import Any
from decimal import Decimal
from uuid import UUID
from classifiedjson.utils import is_match
from logging import getLogger


logger = getLogger(__name__)


#TODO: uuid and decimal, complex

def serialize_scalars(obj: Any) -> Any:
    # checking dict and list last because it's for inherited dict/list only
    # thus not as common as native dict/list which are handled by encoder
    # this provides a default serailization for inherited dict/list
    if is_match(obj, Decimal):
        logger.debug("serialize decimal")
        # convert tuples to list to minimize serialization overhead, list is native
        t = obj.as_tuple()
        l = list(t)
        l[1] = list(l[1])
        return l
    elif is_match(obj, UUID):
        logger.debug("serialize UUID")
        return str(obj)
    elif is_match(obj, str):
        logger.debug("serialize standard str")
        return str(obj)
    elif is_match(obj, int):
        logger.debug("serialize standard int")
        return int(obj)
    elif is_match(obj, float):
        logger.debug("serialize standard float")
        return float(obj)
    else:
        return NotImplemented


def deserialize_scalars(factory: Factory, obj: Any):
    if factory.is_match(Decimal):
        obj[1] = tuple(obj[1])
        t = tuple(obj)
        return Decimal(t)
    elif factory.is_match((UUID, str, int, float)):
        return factory(obj)
    else:
        raise TypeError(
            f"Wrong type.  Expected a scalar type (Decimal, UUID, str, int, float) but received '{factory}' for deserializaiton")
