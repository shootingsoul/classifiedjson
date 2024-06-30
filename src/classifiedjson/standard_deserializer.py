# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from typing import Dict, List, Callable
from classifiedjson.kind_enum import Kind
from classifiedjson.kind_serialization import deserialize_kind
from logging import getLogger


logger = getLogger(__name__)


class StandardDeserializer:
    def __init__(self, builtin_kind_hooks: Dict[Kind, Callable]):
        self._kind_hooks = builtin_kind_hooks

    def deserialize_dict(self, data: Dict):
        # all dicts are native kinds
        # so we are using the standard jsondecoder and overiding the object handling
        kind_data = deserialize_kind(data)
        kind = kind_data.kind
        hook_result = NotImplemented
        try:
            logger.debug("deserialize kind: " + kind.name)
            deserialize_hook = self._kind_hooks.get(kind)
            if deserialize_hook is not None:
                if isinstance(deserialize_hook, list):
                    # list of hooks, e.g. custom
                    # return first implementation
                    for hook in deserialize_hook:
                        hook_result = hook(kind_data.factory, kind_data.obj)
                        if hook_result != NotImplemented:
                            break
                else:
                    hook_result = deserialize_hook(
                        kind_data.factory, kind_data.obj)
            else:
                raise ValueError(
                    f"Invalid schema.  The kind {kind.name} is not supported for decoding.")
        except Exception as exc:
            raise ValueError(f"Decoding error for kind={kind.name}") from exc

        if hook_result == NotImplemented:
            raise RuntimeError(
                f"No function found to deserialize the data for kind={kind.name}")
        else:
            return hook_result
