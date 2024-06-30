# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from classifiedjson.factory import Factory
from typing import Any
from classifiedjson.utils import is_match
from logging import getLogger
from datetime import datetime, timezone, timedelta


logger = getLogger(__name__)


def serialize_datetime(obj: Any) -> Any:
    if not is_match(obj, datetime):
        return NotImplemented

    logger.debug("serialize datetime")

    z = timezone.utc
    z.utcoffset
    ts = obj.timestamp()
    if obj.tzinfo is None:
        return [ts]

    offset_seconds = obj.tzinfo.utcoffset(obj).seconds
    if offset_seconds == 0:
        return [ts, 0]
    else:
        name = obj.tzinfo.tzname(obj)
        return [ts, offset_seconds, name]


def deserialize_datetime(factory: Factory, obj: Any):
    if not factory.is_match(datetime):
        raise TypeError(
            f"Wrong type.  Expected type enum but received '{factory}' for deserializaiton")

    ts = obj[0]
    tz = None
    size = len(obj)
    if size == 2:
        tz = timezone.utc
    elif size == 3:
        td = timedelta(seconds=obj[1])
        tz = timezone(td, obj[2])

    dt = datetime.fromtimestamp(ts, tz)
    return dt
