# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from typing import Any, TextIO, List, Callable, Union
from classifiedjson.kind_enum import Kind
from classifiedjson.standard_deserializer import StandardDeserializer
from classifiedjson.standard_serializer import StandardSerializer, HookItem
from classifiedjson.standards.containers import deserialize_containers, serialize_contianers
from classifiedjson.standards.dataclass import deserialize_dataclass, serialize_dataclass
from classifiedjson.standards.enum import deserialize_enum, serialize_enum
from classifiedjson.standards.custom_attribute import deserialize_custom_attribute, serialize_custom_attribute
from classifiedjson.standards.datetime import serialize_datetime, deserialize_datetime
from classifiedjson.standards.scalars import serialize_scalars, deserialize_scalars
from classifiedjson.natives.dict import encode_dict, deserialize_dict
from classifiedjson.natives.array import deserialize_array, encode_array
from classifiedjson.natives.bytes import encode_bytes, deserialize_bytes
from io import StringIO
import json

from classifiedjson.standards.scalars import serialize_scalars


def dump(obj: Any,
         fp: TextIO,
         custom_hooks: Union[Callable, List[Callable]] = []):
    """Serialize ``obj`` as a Classified JSON formatted stream to ``fp`` (a
    ``.write()``-supporting IO stream).

    ``custom_hooks(obj)`` is a function or list of functions that return a serializable version
    of obj or return NotImplemented.
    """
    serializer = _build_serializer(fp, custom_hooks)
    serializer.serialize(obj)


def dumps(obj: Any,
          custom_hooks: Union[Callable, List[Callable]] = []) -> str:
    """Serialize ``obj`` to a Classified JSON formatted ``str``.

    ``custom_hooks(obj)`` is a function or list of functions that return a serializable version
    of obj or return NotImplemented.
    """
    fp = StringIO()
    dump(obj, fp, custom_hooks)
    return fp.getvalue()


def load(fp: TextIO,
         custom_hooks: Union[Callable, List[Callable]] = []):
    """Deserialize ``fp`` (a ``.read()``-supporting IO stream object containing
    a Classified JSON document) to a Python object.

    ``custome_hooks(factory: Factory, obj)`` is a function or list of functions that 
    return a deserialized version of obj or return NotImplemented.
    """
    
    deserializer = _build_deserializer(custom_hooks)
    return json.load(fp, object_hook=deserializer.deserialize_dict)


def loads(s: Union[str, bytes],
          custom_hooks: Union[Callable, List[Callable]] = []) -> str:
    """Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing a Classified JSON document) to a Python object. 

    ``custome_hooks(factory: Factory, obj)`` is a function or list of functions that 
    return a deserialized version of obj or return NotImplemented.
    """

    deserializer = _build_deserializer(custom_hooks)
    return json.loads(s, object_hook=deserializer.deserialize_dict)


def _build_deserializer(custom_hooks: List[Callable]) -> StandardDeserializer:
    d = {}
    d[Kind.DATACLASS] = deserialize_dataclass
    d[Kind.ENUM] = deserialize_enum
    d[Kind.CUSTOM] = custom_hooks
    d[Kind.CUSTOM_ATTRIBUTE] = deserialize_custom_attribute
    d[Kind.DATETIME] = deserialize_datetime
    d[Kind.DICT] = deserialize_dict
    d[Kind.ARRAY] = deserialize_array
    d[Kind.BYTES] = deserialize_bytes
    d[Kind.CONTAINERS] = deserialize_containers
    d[Kind.SCALARS] = deserialize_scalars
    deserializer = StandardDeserializer(d)
    return deserializer


def _build_serializer(fp: TextIO,
                      custom_hooks: List[Callable] = None) -> StandardSerializer:

    # order matters.  hooks higher in the list are processed first
    # after a hook processes an obj no other hook processes it
    hooks = []
    # first hooks passed directly to dump/load have priority over attribute hooks
    if isinstance(custom_hooks, list):
        for custom_hook in custom_hooks:
            hooks.append(HookItem(Kind.CUSTOM, custom_hook))
    elif custom_hooks:
        hooks.append(HookItem(Kind.CUSTOM, custom_hooks))
    hooks.append(HookItem(Kind.CUSTOM_ATTRIBUTE, serialize_custom_attribute))
    hooks.append(HookItem(Kind.DATACLASS, serialize_dataclass))
    hooks.append(HookItem(Kind.ENUM, serialize_enum))
    hooks.append(HookItem(Kind.DATETIME, serialize_datetime))
    hooks.append(HookItem(Kind.CONTAINERS, serialize_contianers))
    hooks.append(HookItem(Kind.SCALARS, serialize_scalars))

    # Native encoder hooks
    encoder_hooks = []
    encoder_hooks.append(HookItem(Kind.DICT, encode_dict))
    encoder_hooks.append(HookItem(Kind.BYTES, encode_bytes))
    encoder_hooks.append(HookItem(Kind.ARRAY, encode_array))

    s = StandardSerializer(fp, hooks, encoder_hooks)
    return s
