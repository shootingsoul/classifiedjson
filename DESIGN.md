# Classified JSON Design

## Goals

- Preserve origianl type Information
    - Whatever type was serialized is what is deserialized
- Preserve original value
    - close as possible for a functional equivalent
    - **byte match of all internal state is not a goal**
- Support commonly used data types
    - e.g. dict, dataclasses, list, float, datetime, etc.
    - work on all subclasses of supported types
    - No need to add more type-hints, etc.
    - works out of the box on these types
- Work with arbitrary typed data
    - doesn't need to match existing type-hints or data model
    - deal with reality of what's there
- Minimal API
    - minimize the complexity of the exposed api
    - KISS
- Portability
    - strings are easy to store/load and share around
- Security
    - Check type on deserialization
    - no loading of any code, e.g. no use of importlib
    - json format is battle tested (instead of proposing a new format)
- Extensability
    - allow for users to add serialization support for user defined types
    - allow for users to override default serialization
- Performance
    - optimizing size and/or speed is secondary to the above requirements

---

## Terminology

- **Primative Type:** Exact match between python type and json type. 
    - i.e. str, bool, float, int, list, none
    - dict is not a primative since json limits the key to a str type
- **Native Type:** Native implementation of specific types for performance optimization. 
    - e.g. dict, array, ...
- **Standard Type:** Commonly used types we want to support out of the box 
    - e.g. datetime, enum, subclass of dict, ...
- **Encoding:** encode and decode native and primative types to JSON
- **Serializing:** serialize and deserialize standard types to native and primative types
- **Kind:** collection of standard and native types for processing
    - e.g. the 'containers' kind processes all container types (e.g. dict, list, set, frozenset, tuple)
    - e.g. the 'datetime' kind processes only the datetime type

---

## Components

- **Native Encoder**
    - recursively encodes/decodes native and primative types to/from JSON.
    - has direct access to the stream
    - strict, exact type match is used (no subclasses)
    - preserves type information for native types
- **Standard Serializer**
    - recursively serializes/deserializes standard types to/from native and primative types for encoding
    - No direct access to the stream, only has access to the encoder
    - allows for subclass support, doesn't require exact type match
    - preserves type information for standard types
- **Custom Hooks**
    - callable functions defined on a class or passed in to dumps/loads 
    - allows for additional types to be serialized/deserialized
    - allows for overriding the serialization/deserailization of standard types
    - Can **not** override encoding/decoding of native and primative types
- **Factory**
    - has all information needed in order to construct a new instance of a type
    - used on deserialization

---

## Processing Kinds

### Functions

A kind works with native or standard types.  For native types, a kind has functions to encode/decode native types directly to/from the stream.  For standard types, a kind has functions to serailize/deserailize standard types to the encoder.  Every kind for both native and standard has a header to preserve the type information.

For example, the 'array' kind works solely with the array type and has functions encode_array and decode_array to natively encode/decode.  While the 'containers' kind works with a range of container types and has two functions serialize_container and deserialize_container that handles all of the container types.

### Recursion and Order

The native encoder recursively processes all primative and native types.  The first function to handle the object is used and no other function afterwards gets to process that object.  Once an unknown type is encountered, it is given off to the standard serializer for processing.

The standard serailizer recursively processes all standard types and custom hooks.  Custom hooks have priority over standard implementation.  The first function to handle the object is used and no other function afterwards gets to process that object.  Once an unknown type is encountered it throws an unsupported type exception.

This results in the following processing order for an object
1. primative types (exact match, i.e. str, bool, int, float, list, none)
2. native types (exact match, e.g. dict, array, bytes, ...)
3. custom hooks
4. standard types (e.g. subclass dict, datetime, enum, ...)

### Dict

The dict kind handles the python dict object using an exact type match.  It's a native kind that encodes and decodes the python dict as a python list.  It converts a dict to a list as [k1, v1, k2, v2, ...].  

Advantages:
- handles non-str keys since every object in a list is processed independently
- decode directly into a dict as it processes the list each key/value pair at a time
- no need for hidden/dunder fields to inject into a dict
    - type info in stored outside the dict in a kind descriptor

### Subclass Primative and Native Types

Any subclass of a primative or native type is done in a standard kind (e.g. containers kind for dict).  Thus, we have support to serialize any subclass of a primative or native type by default.  However, the serialization of a subclass may be overidden as needed by a custom hook.  All the while the exact native and primative types are processed directly in the encoder and can't be overridden by a custom hook.

### Custom Hooks

A custom hook can be implemented as a function to pass to dump/load or as class attributes.  The hooks passed to dump/load have priority over attribute hooks.  Dump/load accepts a list of hooks which are processed in the order given.

When possible, using attribute hooks is preferred over hooks passed to dump/load.  This is more efficent for processing and easier to manage code deployments for larger systems.

---

## Classified JSON Schema

Every JSON object is a kind descriptor with the type information and object value.  Everything else is a primative type: list, bool, int, str, float, none.

Kind descriptor fields
- **"k":** the kind id integer
- **"f":** a list of type information for the factory
- **"o":** the object value which can be a primative or another kind

Factory descriptor list
- ["t", full_type_name]

The kind descriptor guarentees the order of fields written to allow for efficent decoding of native and primative types by reading the type information to stream the following value directly into the final object.

The factory descriptor list is a dict in list form to give flexibility in the future to store info on how to recreate objects.  Currently it supports the type name, in the future more fields will be added to support generics or other complex situations.

---

## API

The functions for dump, dumps, load and loads are provided and mimic the pattern of similar functions provided by other modules.  It's a well-known interface to use.

To support custom hooks, the Factory class, is_match and is_exact_match functions are exposed.  This is needed to allow for types to be preserved and checked.  On attribute hooks, it allows supporting serailization of subclasses of a custom class.

---

## Implementation Notes

The encoder is written in python and needs to be implemented in rust/c++ with a python wrapper in the future.  This will boost performance improvements for native and primative types significantly.  For now, the standard JSONDecoder is used with the object_hook to process kinds.  This is convenient since all JSON objects are kinds.  The JSONEncoder is only used to process primative scalars with the rest in python since dict handling needed to be overridden.

---
Copyright 2024 Shooting Soul Ventures, LLC
