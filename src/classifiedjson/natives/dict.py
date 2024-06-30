# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from typing import Any, Optional
from logging import getLogger
from classifiedjson.kind_enum import Kind
from classifiedjson.factory import Factory, create_factory
from classifiedjson.kind_serialization import encode_kind_close, encode_kind_open
from classifiedjson.encoder_interface import IEncoder


from classifiedjson.utils import is_exact_match, dict_to_list


logger = getLogger(__name__)


def encode_dict(kind: Kind, encoder: IEncoder, obj: Any) -> Optional[bool]:
    if not is_exact_match(obj, dict):
        return NotImplemented

    logger.debug("encode dict")
    # writing a dict as a list to allow for key type to be anything supported
    # interweave keys and values to allow for fast deserialization in the future
    # for dicts coming from the outside, who knows what type the keys are so don't take the chance

    factory = create_factory(obj)
    l = dict_to_list(obj)

    encode_kind_open(encoder, kind, factory)
    encoder.encode(l)
    encode_kind_close(encoder)
    return True


def deserialize_dict(factory: Factory, obj: Any):
    if not factory.is_exact_match(dict):
        raise TypeError(
            f"Wrong type.  Expected type dict but received '{factory}' for deserializaiton")

    # object is a list of k1, v1, k2, v2 . . . .

    d = {}
    for i in range(0, len(obj), 2):
        # i is the key, i+1 is the value
        d[obj[i]] = obj[i + 1]

    return d
