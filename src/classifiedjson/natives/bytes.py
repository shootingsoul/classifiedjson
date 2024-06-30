# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

import base64
from typing import Any, Optional
from logging import getLogger
from classifiedjson.kind_enum import Kind
from classifiedjson.factory import Factory, create_factory
from classifiedjson.kind_serialization import encode_kind_close, encode_kind_open
from classifiedjson.encoder_interface import IEncoder
from classifiedjson.utils import is_exact_match


logger = getLogger(__name__)


def encode_bytes(kind: Kind, encoder: IEncoder, obj: Any) -> Optional[bool]:
    if not is_exact_match(obj, bytes):
        return NotImplemented
    # encode bytes to b64 string,
    # FUTURE ideally write this to the stream in directly
    encoded = base64.b64encode(obj)
    value_str = encoded.decode("utf-8")

    encode_kind_open(encoder, kind, create_factory(obj))
    encoder.encode(value_str)
    encode_kind_close(encoder)
    return True


def deserialize_bytes(factory: Factory, obj: Any):
    if not factory.is_exact_match(bytes):
        raise TypeError(
            f"Wrong type.  Expected type array but received '{factory}' for deserializaiton")
    b = obj.encode("utf-8")
    decoded_bytes = base64.b64decode(b)
    return decoded_bytes
