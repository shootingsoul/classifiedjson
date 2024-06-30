# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from typing import Dict
from classifiedjson.kind_enum import Kind
from classifiedjson.kind_data import KindData
from classifiedjson.factory import Factory, deserialize_factory, serialize_factory
from classifiedjson.encoder_interface import IEncoder
from logging import getLogger


logger = getLogger(__name__)


# split up kind object writing to allow native encoders to directly stream the value
def encode_kind_open(encoder: IEncoder, kind: Kind, factory: Factory):
    # write the order as Kind, Factory (type info), Object
    # this way deserailization can be optimized
    # first get the kind, then the type info then deserailized the object for that type . . .
    encoder.write('{"k":')
    encoder.write(str(kind.value))
    encoder.write(',"f":')
    encoder.encode(serialize_factory(factory))
    encoder.write(',"o":')


def encode_kind_close(encoder: IEncoder):
    encoder.write('}')


def deserialize_kind(data: Dict):
    # only deserailize the wrapper, not the value.  Leave that for the type specific functions
    kind_id = data.get("k")
    if kind_id is None:
        raise ValueError(
            f"Invalid schema for kind data.  Dict key 'k' is missing.")
    try:
        kind = Kind(int(kind_id))
    except:
        raise ValueError(
            f"Invalid schema for kind data.  The kind enum value '{kind_id}' is invalid.")

    # after calling this verify the type is what you want (e.g. dataclass, etc.)
    factory_data = data.get("f")
    if factory_data is None:
        raise ValueError(
            f"Invalid schema for kind data.  Dict key 'f' is missing.")
    factory = deserialize_factory(factory_data)

    # None is a valid value so need to check key explicitly
    if 'o' not in data:
        raise ValueError(
            f"Invalid schema for kind data.  Dict key 'o' is missing.")
    obj = data['o']

    return KindData(kind, factory, obj)
