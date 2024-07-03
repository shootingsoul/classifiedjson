# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

import math
from typing import Any, Optional
from logging import getLogger
from classifiedjson.kind_enum import Kind
from classifiedjson.factory import Factory, create_factory
from classifiedjson.kind_serialization import encode_kind_close, encode_kind_open
from classifiedjson.encoder_interface import IEncoder


from classifiedjson.utils import is_exact_match, dict_to_list


logger = getLogger(__name__)


def encode_float_special(kind: Kind, encoder: IEncoder, obj: Any) -> Optional[bool]:
    # NOTE: called directly after check for float isfinite
    #       so no need to recheck the type

    logger.debug("encode float special")
    # writing a dict as a list to allow for key type to be anything supported
    # interweave keys and values to allow for fast deserialization in the future
    # for dicts coming from the outside, who knows what type the keys are so don't take the chance

    factory = create_factory(obj)

    # already know it's a special float of nan, inf or -inf
    if math.isnan(obj):
        v = 0   # nan
    elif obj > 0:
        v = 1   # inf
    else:
        v = -1  # -inf

    encode_kind_open(encoder, kind, factory)
    encoder.encode(v)
    encode_kind_close(encoder)
    return True


def deserialize_float_special(factory: Factory, obj: Any):
    if not factory.is_exact_match(float):
        raise TypeError(
            f"Wrong type.  Expected type float but received '{factory}' for deserializaiton")

    if obj == 0:
        return float("nan")
    elif obj > 0:
        return float("inf")
    else:
        return float("-inf")
