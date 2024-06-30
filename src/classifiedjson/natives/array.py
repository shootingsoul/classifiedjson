# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from array import array
from typing import Any, Optional
from logging import getLogger
from classifiedjson.kind_enum import Kind
from classifiedjson.factory import Factory, create_factory
from classifiedjson.kind_serialization import encode_kind_close, encode_kind_open
from classifiedjson.encoder_interface import IEncoder
from classifiedjson.utils import is_exact_match


logger = getLogger(__name__)


def encode_array(kind: Kind, encoder: IEncoder, obj: Any) -> Optional[bool]:
    if not is_exact_match(obj, array):
        return NotImplemented

    # FUTURE: optimize by writing value directly to the stream
    res = []
    res.append(obj.typecode)

    if obj.typecode == 'u':
        # we can to array unicode as a string
        value = obj.tounicode()
    else:
        value = obj.tobytes()
    res.append(value)

    encode_kind_open(encoder, kind, create_factory(obj))
    encoder.encode(res)
    encode_kind_close(encoder)
    return True


def deserialize_array(factory: Factory, obj: Any):
    if not factory.is_exact_match(array):
        raise TypeError(
            f"Wrong type.  Expected type array but received '{factory}' for deserializaiton")

    typecode = obj[0]
    value = obj[1]
    a = array(typecode, value)
    return a
