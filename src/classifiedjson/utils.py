# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

import typing
from typing import Any, Dict, Type, Tuple, Union, List


def get_type_name(cls: Type) -> str:
    # combine module and class for the type name
    return f"{cls.__module__}.{cls.__name__}"


def split_type_name(full_type_name: str) -> Tuple[str, str]:
    # split full type name into module and class names
    i = full_type_name.rindex('.')
    module_name = full_type_name[:i]
    class_name = full_type_name[i + 1:]
    return module_name, class_name


def is_match(obj, classinfo: Union[Type, Tuple[Type]]) -> bool:
    """Verify the object is of a type or subclass of the type in the list

    ``obj`` instance object to check the type of

    ``classinfo`` is a type or list of types to check if  
    the obj is an instance of the type or subclass of that type
    """
    cls = type(obj)
    if isinstance(classinfo, list):
        for c in classinfo:
            if issubclass(cls, c):
                return True
        return False
    else:
        return issubclass(cls, classinfo)


def is_exact_match(obj: Any, classinfo: Union[Type, Tuple[Type]]) -> bool:
    """Verify the object is of the exact type or one of the exact types in the list

    ``obj`` instance object to check the type of

    ``classinfo`` is a type or list of types to check if  
    the obj is an instance of that exact type
    """
    cls = type(obj)
    if isinstance(classinfo, list):
        for c in classinfo:
            if cls == c:
                return True
        return False
    else:
        return cls == classinfo


def dict_to_list(obj: Dict) -> List:
    if obj is None:
        return None

    l = []
    for key, value in obj.items():
        l.append(key)
        l.append(value)
    return l


def list_to_dict(obj: List) -> Dict:
    if obj is None:
        return None

    d = {}
    for i in range(0, len(obj), 2):
        # i is the key, i+1 is the value
        d[obj[i]] = obj[i + 1]
    return d
