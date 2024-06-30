# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from typing import Any, TextIO, List
from logging import getLogger
from classifiedjson.factory import create_factory
from classifiedjson.native_encoder import NativeEncoder
from classifiedjson.hook_item import HookItem
from classifiedjson.kind_serialization import KindData


logger = getLogger(__name__)


class StandardSerializer:
    def __init__(self,
                 stream: TextIO,
                 hooks: List[HookItem],
                 encoder_hooks: List[HookItem]):
        self._native = NativeEncoder(
            stream, self._process_hooks, encoder_hooks)
        self._hooks = hooks

    def serialize(self, obj: Any):
        # kick off the process
        self._native.encode(obj)

    def _process_hooks(self, obj: Any):
        # encoding chugs along on native obj until it encounters a foriegner
        # let's see if we can translate . . .

        # logger.debug("Processing serialization hooks for %s", get_type_name(type(obj)))
        # go through all the hooks.  First hook to process the item is returned
        # it's wrapped in a kind wrapper to preserve the type info for deserialization
        for hook_item in self._hooks:
            hook = hook_item.hook
            # logger.debug("calling serializer hook = %s on obj of type = %s", hook.__name__, get_type_name(type(obj)))
            try:
                hook_result = hook(obj)
                if hook_result == NotImplemented:
                    # hook doesn't understand the type
                    continue
                else:
                    factory = create_factory(obj)
                    logger.debug(
                        "handled by hook serializer (hook=%s obj_cls=%s)", hook.__name__, factory)
                    return KindData(hook_item.kind, factory, hook_result)
            except Exception as exc:
                # rethrow with hook name for context
                raise RuntimeError(
                    f"Error processing serializer hook '{hook.__name__}'") from exc

        # object not handled by native or hooks
        type_name = type(obj).__name__
        raise RuntimeError(
            f"The type '{type_name}' is not supported for serialization.  Add a hook to support it.")
