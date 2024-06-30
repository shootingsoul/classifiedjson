# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from tests.utils import dumps_and_loads


def test_nozone():
    # preserve no timezone if not set
    dt = datetime.now()
    d = dumps_and_loads({"dt": dt})
    dt_plain = d["dt"]
    assert dt_plain.tzinfo is None
    assert dt.timestamp() == dt_plain.timestamp()


def test_la():
    dt_zone = datetime.now().astimezone(ZoneInfo("America/Los_Angeles"))
    d = dumps_and_loads({"dt_zone": dt_zone})
    dtz = d["dt_zone"]

    assert dtz.tzinfo is not None
    assert dtz.timestamp() == dt_zone.timestamp()
    assert dtz.tzname() == dt_zone.tzname()

    offset = dt_zone.tzinfo.utcoffset(dt_zone)
    offset2 = dtz.tzinfo.utcoffset(dtz)
    assert offset.seconds == offset2.seconds


def test_utc():
    dt_zone = datetime.now().astimezone(timezone.utc)
    d = dumps_and_loads({"dt_zone": dt_zone})
    dtz = d["dt_zone"]

    assert dtz.tzinfo is not None
    assert dtz.timestamp() == dt_zone.timestamp()
    assert dtz.tzname() == dt_zone.tzname()

    offset = dt_zone.tzinfo.utcoffset(dt_zone)
    offset2 = dtz.tzinfo.utcoffset(dtz)
    assert offset.seconds == offset2.seconds


def test_remote():
    dt_zone = datetime.now().astimezone(ZoneInfo("Pacific/Fakaofo"))
    d = dumps_and_loads({"dt_zone": dt_zone})
    dtz = d["dt_zone"]

    assert dtz.tzinfo is not None
    assert dtz.timestamp() == dt_zone.timestamp()
    assert dtz.tzname() == dt_zone.tzname()

    offset = dt_zone.tzinfo.utcoffset(dt_zone)
    offset2 = dtz.tzinfo.utcoffset(dtz)
    assert offset.seconds == offset2.seconds
