# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from typing import Any


class IEncoder:
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return "IEncoder()"

    def write(self, text: str) -> None:
        pass

    def encode(self, obj: Any) -> None:
        pass
