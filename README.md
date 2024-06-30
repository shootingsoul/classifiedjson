# Classified JSON

Preserve types when dumping and loading data with json
- works on arbitrary typed data without pre-determined type-hints or data model
- supports dataclasses, dict with non-str keys, subclasses and more . . .
- Add custom hooks to support your own classes
- loads types recursively, including custom hooks
- Outputs to standard JSON

The serialized JSON content is solely for deserailizing back into Python.  It is not meant to be human readable and is considered _**classified**_.  It's off the record, on the qt, and very, very hush, hush.   

```
pip install classifiedjson
```
```python
from enum import Enum
from dataclasses import dataclass
from classifiedjson import dumps, loads

class Status(Enum):
    IDLE = 0
    RUNNING = 1
    STOPPING = 2

@dataclass
class Job:
    name: str

jobs = {}
jobs[Status.IDLE] = [Job("a"), Job("b")]
jobs[Status.RUNNING] = [Job("x"), Job("y"), Job("z")]

serialized = dumps(jobs)

# ... tempus fugit...
old_jobs = loads(serialized)
print([j.name for j in old_jobs[Status.RUNNING]])
```
output
```
['x', 'y', 'z']
```

---

## Supported Types

- dataclasses
- dict (including non-string keys)
- list, tuple, set, frozenset
- str, int, bool, float, None
- enum, datetime
- array, bytes
- any subclasses of the above types

---

## Installation

Python >=3.8
```
pip install classifiedjson
```

---

## Examples

### dataclass with arbitray typed data from the wild
```python
from dataclasses import dataclass
from classifiedjson import dumps, loads

@dataclass
class Cat:
    def speak(self) -> str:
        return 'meow'

@dataclass
class House:
    pet: Cat

@dataclass
class WildGator:
    def speak(self):
        return 'chomp'

house = House(WildGator())
print(house.pet.speak())
serialized = dumps(house)

# ... later gator...
old_house = loads(serialized)
print(old_house.pet.speak())
```
#### output
```
chomp
chomp
```
---
### dict with non-string keys
```python
from enum import Enum
from classifiedjson import dumps, loads

class DayPart(Enum):
    MORNING = 0
    NOON = 1
    NIGHT = 2

forecast = {}
forecast[DayPart.MORNING] = "rainy"
forecast[DayPart.NOON] = "cloudy"
forecast[DayPart.NIGHT] = "sunny"

serialized = dumps(forecast)

# ... just over that ridge...
old_forecast = loads(serialized)
print(old_forecast[DayPart.NOON])
```
#### output
```
cloudy
```
---
### list subclass
```python
from enum import Enum
from classifiedjson import dumps, loads

class MyList(list):
    def avg(self):
        return sum(self)/len(self)
        
my_list = MyList([18,90,26,70,47,1])
print(my_list.avg())
serialized = dumps(my_list)

# ... some time later...
old_list = loads(serialized)
print(old_list.avg())
```
#### output
```
42.0
42.0
```

---

## Custom Hooks

Add support to load and dump your own classes

```python
from classifiedjson import dumps, loads, Factory
from enum import Enum

class Operator(Enum):
    ADD = 1
    MULTIPLY = 2

class Mathy:
    def __init__(self, data: list[int], operator: Operator ) -> None:
        self._data = data
        self._operator = operator
        self.scratch_notes: str = ""

    def __str__(self):
        return f"{self._data} scratch={self.scratch_notes}"

    def operate(self, value: int):
        if self._operator == Operator.ADD:
            self._data = list(map(lambda x: x + value, self._data)) 
        else:        
            self._data = list(map(lambda x: x * value, self._data)) 
    
    def classifiedjson_serialize(self):
        # save what we want
        return { 'data': self._data, 'operator': self._operator}

    @classmethod
    def classifiedjson_deserialize(cls, factory: Factory, obj):
        # call constructor with serailized data
        return factory(data=obj['data'], operator=obj['operator'])


workspace = Mathy([1,3,5,7,11], Operator.ADD)
workspace.scratch_notes = "Hmm, I like dark chocolate"
workspace.operate(5)
print(workspace)
serialized = dumps(workspace)

# ... keep on truckin'....
old_workspace = loads(serialized)
old_workspace.operate(1)
print(old_workspace)
```
output
```
[6, 8, 10, 12, 16] scratch=Hmm, I like dark chocolate
[7, 9, 11, 13, 17] scratch=
```

---

Override how datetime is serailized with a custom hook function

```python
from classifiedjson import dumps, loads, Factory, is_exact_match
from datetime import datetime, timezone

# the default datetime serialization preserves whatever timezone is there or not.
# So if there is no timezone, then it leaves it without one.
# here's how we can force a timezone to utc

def dt_serialize(obj):
    if not is_exact_match(obj, datetime):
        return NotImplemented

    # e.g. datetime serialize to force timezone to utc
    timestamp = obj.astimezone(timezone.utc).timestamp()
    return timestamp

def dt_deserialize(factory: Factory, obj):
    if not factory.is_exact_match(datetime):
        return NotImplemented

    return datetime.fromtimestamp(obj, timezone.utc)

def print_dt(dt):
    tz = "<none>" if dt.tzinfo is None else dt.tzname()
    print(f"{dt} zone={tz}")

dt = datetime(year=2024, month=2, day=2, hour=9, minute=1)
print_dt(dt)
serialized = dumps(dt, [dt_serialize])

# ...tempus fugit...
# yes, you can add as many custom hook functions as needed
dt_utc = loads(serialized, [dt_deserialize])
print_dt(dt_utc)
```
output (example)
```
2024-02-02 09:01:00 zone=<none>
2024-02-02 14:01:00+00:00 zone=UTC
```

## Security

- No modules are loaded
- All data is type checked on deserialization

---
Copyright 2024 Shooting Soul Ventures, LLC
