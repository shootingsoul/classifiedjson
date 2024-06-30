# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from enum import Enum


class Kind(Enum):
    DICT = 0
    DATACLASS = 1
    ENUM = 2
    DATETIME = 3
    CUSTOM = 4
    CUSTOM_ATTRIBUTE = 5
    ARRAY = 6
    BYTES = 7
    CONTAINERS = 8
    SCALARS = 9
