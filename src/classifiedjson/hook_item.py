# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from typing import Callable
from classifiedjson.kind_enum import Kind


class HookItem:
    # used for serializer, encoder or deserializer
    def __init__(self, kind: Kind, hook: Callable) -> None:
        self.kind = kind
        self.hook = hook
