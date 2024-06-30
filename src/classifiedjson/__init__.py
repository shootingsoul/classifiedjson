# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from classifiedjson.api import dump, dumps, load, loads
from classifiedjson.factory import Factory
from classifiedjson.utils import is_exact_match, is_match

__version__ = '1.0.0'
__all__ = (__version__,
           dump,
           dumps,
           load,
           loads,
           is_exact_match,
           is_match,
           Factory)
