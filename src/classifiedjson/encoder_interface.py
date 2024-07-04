# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from typing import Any, Protocol


class IEncoder(Protocol):

    def write(self, text: str) -> None:
        pass

    def encode(self, obj: Any) -> None:
        pass
