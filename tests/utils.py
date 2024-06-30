# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from classifiedjson import dumps, loads
from logging import getLogger

logger = getLogger(__name__)


def dumps_and_loads(v):
    s = dumps(v)
    if len(s) == 0:
        logger.warning("serialization returned empty string")
    else:
        logger.debug(s)
    return loads(s)
