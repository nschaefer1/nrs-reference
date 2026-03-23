
# Class Utilities

## Constructor & Initialization

`__init__` (Constructor)

The constructor initializes a new instance of a class. This is called automatically when creating an object and used to set initial state.

```python
class MyClass:
    def __init__(self, value):
        self.value = value
```

## Post Initialization

`__post_init__` (Dataclasses)

Runs after `__init__` in dataclasses. Useful for validation or derived values.

```python
from dataclasses import dataclass

@dataclass
class MyClass:
    x: int

    def __post_init__(self):
        self.x *= 2
```

## Cleanup, Destruction & Resource Management

`__del__` (Destructor)

Called when an object is about to be destroyed. Not reliable for critical cleanup, execution timing is unpredictable, and avoid for important resource handling.

```python
class MyClass:
    def __del__(self):
        print("Cleaning up")
```

## Context Managers

The preferred way to manage resources. Guaranteeds cleanup, works if errors occur, best practice for files, connections, etc.

```python
class MyResource:
    def __enter__(self):
        print("Start")
        return self

    def __exit__(self, exc_type, exc, tb):
        print("Cleanup")

with MyResource():
    print("Using resource")
```

**Using `contextlib`**

```python
from contextlib import contextmanager

@contextmanager
def my_resource():
    print("Start")
    yield
    print("Cleanup")
```

## Properties

Encapsulates attribute access with logic. Allows validation and computed attributes, keeps external interface clean. 

```python
class MyClass:
    def __init__(self):
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val < 0:
            raise ValueError("Must be positive")
        self._value = val
```

**Read-only property**

No setter → read-only

```python
@property
def value(self):
    return self._value
```

## Static Methods

No access to instance self or class. Just namspaced utility functions.

```python
class MyClass:
    @staticmethod
    def helper(x):
        return x * 2
```

## Class Methods

Operate on class-level data. Often used for factories.

```python
class MyClass:
    count = 0

    @classmethod
    def increment(cls):
        cls.count += 1
```

## Default Methods

Default methods can be implemented with a purposeful error to force each class to have a method and if the method isn't implemented properly, than it throws an error.

```python
class MainClass(BaseClass):
    def __init__(self):
        pass

class BaseClass:
    def default_method(self):
        raise NotImplementedError("Class much implement run_etl")

MainClass().default_method()    # ← This will error unless MainClass contains default_method override
```