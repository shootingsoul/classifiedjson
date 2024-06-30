# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from classifiedjson.kind_enum import Kind
from classifiedjson.factory import Factory
from typing import Any


class KindData:
    def __init__(self, kind: Kind, factory: Factory, obj: Any):
        self.kind = kind
        self.factory = factory
        self.obj = obj
