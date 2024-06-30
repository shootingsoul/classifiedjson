# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

import sys
from typing import List, Type, Any, Dict, Tuple, Union
from classifiedjson.utils import dict_to_list, get_type_name, list_to_dict, split_type_name
from logging import getLogger


logger = getLogger(__name__)


# factory to recreate an object of a single, specific type
# there are separate, new factories for each type to deal with

# factory has the type info needed to recreate obj
# has type checking functions for security
# callable, so make a call on the class to recreate the obj


class Factory:
    """Factory creates a typed instance of an object.
    The factory itself is callable where constructor args and kwargs are given to create the object

    For example: my_typed_obj = factory(data)
    """
    def __init__(self, type_name: str):
        self._type_name = type_name
        self._cls = None

    def __repr__(self):
        return f"Factory({self._type_name})"

    def __str__(self):
        return f"{self._type_name}"

    def is_match(self, classinfo: Union[Type, Tuple[Type]]) -> bool:
        """Verify the factory will create an object of a type or subclass of the type in the list

        ``classinfo`` is a type or list of types to check if the factory 
        will create an instance of the type or subclass of that type
        """
        cls = self._get_cls()
        if isinstance(classinfo, list):
            for c in classinfo:
                if issubclass(cls, c):
                    return True
            return False
        else:
            return issubclass(cls, classinfo)

    def is_exact_match(self, classinfo: Union[Type, Tuple[Type]]) -> bool:
        """Verify the factory will create an object of a exact type in the list

        ``classinfo`` is a type or list of types to check if the factory 
        will create an instance of the exact type
        """
        cls = self._get_cls()
        if isinstance(classinfo, list):
            for c in classinfo:
                if cls == c:
                    return True
            return False
        else:
            return cls == classinfo

    def __call__(self, *args, **kwargs):
        # recreate object from type info in factory and deserialized data passed in
        cls = self._get_cls()
        return cls(*args, **kwargs)

    def _get_cls(self) -> Type:
        if not self._cls:
            self._cls = _get_loaded_type(self._type_name)
        return self._cls


def create_factory(obj: Any) -> Factory:
    # create factory in order to recreate the obj
    factory = Factory(get_type_name(type(obj)))
    return factory

# Factory is visible to users, so be sure to keep the class methods clean

# NOTE: factory data is serialized to the metadata of the kind header
#       thus it can't use dict directly.  Convert any dict to a list ahead of time
#       that's because Dict kind itself needs a header which includes factory


def serialize_factory(factory: Factory) -> List:
    # serialize as a dict 'cuz it's gonna get crazy
    # with a dict we can add/remove whatever fields we need to reconstruct and obj
    data = {"t": factory._type_name}

    # serialize as a list because it's in the metadata of the kind object
    # only kind is allowed to be a dict
    return dict_to_list(data)


def deserialize_factory(obj: List) -> Factory:
    d = list_to_dict(obj)

    type_name = d.get('t')
    if type_name is None:
        raise ValueError(
            f"Invalid schema for kind data factory.  Dict key 't' is missing.")

    return Factory(type_name)


def _get_loaded_type(full_type_name: str, ignore_not_found: bool = False) -> Type:
    # given a full type name, find the class type in a module that's already loaded
    # NOTE: always check the type is what you want
    #       after calling this function to help guard against hackers
    module_name, class_name = split_type_name(full_type_name)

    # type must already be imported
    if module_name not in sys.modules:
        if ignore_not_found:
            return None
        raise RuntimeError(
            f"Module not found for {full_type_name}.  Import the module.")
    module = sys.modules[module_name]

    class_type = getattr(module, class_name, None)
    if class_type is None:
        if ignore_not_found:
            return None
        raise TypeError(
            f"Class '{class_name}' not found in the module '{module_name}'.")

    return class_type
