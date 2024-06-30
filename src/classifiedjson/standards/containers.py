# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from classifiedjson.factory import Factory
from typing import Any, Dict, FrozenSet, List, Set, Tuple
from classifiedjson.utils import is_match
from logging import getLogger


logger = getLogger(__name__)


def serialize_contianers(obj: Any) -> Any:
    # checking dict and list last because it's for inherited dict/list only
    # thus not as common as native dict/list which are handled by encoder
    # this provides a default serailization for inherited dict/list
    if is_match(obj, Tuple):
        logger.debug("serialize tuple")
        return list(obj)
    elif is_match(obj, Set):
        logger.debug("serialize set")
        return list(obj)
    elif is_match(obj, FrozenSet):
        logger.debug("serialize frozenset")
        return list(obj)
    elif is_match(obj, Dict):
        logger.debug("serialize standard dict")
        return dict(obj)
    elif is_match(obj, List):
        logger.debug("serialize standard list")
        return list(obj)
    else:
        return NotImplemented


def deserialize_containers(factory: Factory, obj: Any):
    if factory.is_match((Dict, List, Set, FrozenSet, Tuple)):
        return factory(obj)
    else:
        raise TypeError(
            f"Wrong type.  Expected a container type (dict, list) but received '{factory}' for deserializaiton")
