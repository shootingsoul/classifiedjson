# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from typing import Any, Callable, TextIO, List
from logging import getLogger
from json import JSONEncoder
from classifiedjson.encoder_interface import IEncoder
from classifiedjson.kind_serialization import KindData, encode_kind_open, encode_kind_close

from classifiedjson.utils import get_type_name


logger = getLogger(__name__)

# native types are written directly to the stream in json format
# this is the last level that all serialization comes to

# native recursive call back to encode native objects
# we only kick out of native loop when a non-native object is come across


class NativeEncoder(IEncoder):
    def __init__(self, stream: TextIO, default: Callable, hooks: List[Callable]) -> None:
        super().__init__()
        self._stream = stream
        self._default = default  # to recurse back out
        self._hooks = hooks  # native hooks
        # use standard encoder for scalars
        self._json_encoder = JSONEncoder()

    def _json_encode_and_write(self, obj):
        text = self._json_encoder.encode(obj)
        self._stream.write(text)

    def write(self, text: str):
        self._stream.write(text)

    def encode(self, obj: Any):
        # for native, we do exact type matches only
        # this allows for kind to handle any derived types in order to preserve type info
        cls = type(obj)
        if obj is None:
            self._json_encode_and_write(obj)
        elif cls == bool:
            self._json_encode_and_write(obj)
        elif cls == float:
            self._json_encode_and_write(obj)
        elif cls == int:
            self._json_encode_and_write(obj)
        elif cls == str:
            self._json_encode_and_write(obj)
        elif cls == list:
            self._write_list(obj)
        elif cls == KindData:
            kind_data = obj
            encode_kind_open(self, kind_data.kind, kind_data.factory)
            self.encode(kind_data.obj)
            encode_kind_close(self)
        else:
            if not self._process_hooks(obj):
                # no primative or native supports this object
                # go back out and see if serializer can translate down to native
                self.encode(self._default(obj))

    def _write_list(self, obj: list):
        count = len(obj)
        if count == 0:
            self._stream.write("[]")
        else:
            self._stream.write("[")
            i = 0
            while i < count - 1:
                # recurse back to serialize the item, whatever type it is
                self.encode(obj[i])
                self._stream.write(', ')
                i += 1

            # write the last item
            self.encode(obj[i])
            self._stream.write("]")

    def _process_hooks(self, obj: Any) -> bool:

        # logger.debug("Processing encoder hooks for %s", get_type_name(type(obj)))
        # go through all the hooks.  First hook to process the item is returned
        # it's wrapped in a kind wrapper to preserve the type info for deserialization
        for hook_item in self._hooks:
            kind = hook_item.kind
            hook = hook_item.hook
            try:
                handled = hook(kind, self, obj)
                if handled == NotImplemented:
                    continue
                elif type(handled) == bool:
                    if handled:
                        logger.debug("handled by hook encoder (hook=%s obj_cls=%s)",
                                     hook.__name__, get_type_name(type(obj)))
                        return True
                else:
                    raise ValueError(
                        f"Encoder hook must return a bool indicating if obj was handled or not. ({hook.__name__})")
            except Exception as exc:
                # rethrow with hook name for context
                raise RuntimeError(
                    f"Error processing encoder hook '{hook.__name__}'") from exc

        # no hook handled it
        return False
