# PySignature

PySingature is a python package that provides a set of utilities
for simple function parameter typechecking, without modifying
the target function and with minimal boilerplate or impact
on performance.

## Usage

PySignature provides two main components: a small set of
classes that represent type assertions and a decorator for defining
the function's signature.

### Example

Let's take a look at a (very) simple function:

```python
def fn(x, y):
    return x * y
```

We can add parameter typechecking using the PySignature in the
following way:

```python
from pysignature import typechecked
from pysignature.types import Numeric

@typechecked(x=Numeric, y=Numeric)
def fn(x, y):
    return x + y
```

Now if we call `fn` with non-numeric types (neither ints nor floats)
we get an exception `FunctionTypeCheckError` with detailed information
about the wrong parameters in its property `errors`.

### Complex type assertions

We can go beyond numeric validation and use complex type assertions
provided by this module, or we can use any callable that uppon error
returns a `TypeError` (such as `float`).

To expand our previous example, let's consider the fact that the `*`
operator works if the left operand is a list or a string and the right
operand is an integer (`Numeric` accepts floats). We can make use
of built-in function `int` and PySignature's `List`, `Or`, `List` and `Any`
type assertions.

```python
from pysignature import typechecked
from pysignature.types import String, Or, List, Any

@typechecked(x=Or(String, List(Any)), y=int)
def fn(x, y):
    return x + y
```

### Variadic and keyword arguments

PySignature supports typechecking for `*args` and `**kwargs` argument
types. The only limitation is that they all must conform to a single
type. They are specified in the following way:

```python
@typechecked(x=String, _variadic=Numeric, _named=List(List(Any)))
def fn(x, *extra, **options):
    # ... Do something
    return
```

### Bypassing typechecks

Each function decorated with `pysignature.typechecked` gets
a property named `untyped` that ignores the typechecking
functionality. In our original example, that would mean
we can use `fn.untyped(None, 1)`.

## Rationale

PySignature was created to cover a very specific need: allow
for robust handling of parameters coming from the external world
(the internet) without burdening the data scientists at
[Intelimétrica](https://intelimetrica.com/) with the fact
that their functions might be called with unsafe arguments.

The idea is to use PySignature in the (normally) small subset
of functions that are exposed from a certain module to the
outside world, so the mantainers of the function can develop
without extra cognitive burden and the clients of such function
can use them with extra confidence and robustness.

## What PySignature is not

PySignature is not (neither tries to be) an extension to Python's
type system. It does not attempt to bring full static typying
to the languge and while it is not slow, it is not recommended
for functions that are too be called in very tight loops.

## Installation

Simply install via pip with:

```
$ pip install pysignature
```

Or, directly download the package and run

```
$ python setup.py install
```

## Contribute

Yes please! Help us with documentation, reporting bugs,
implementing new type assertions or improving code

The development requirements are minimal. The only consideration
is that we use [pytest](https://github.com/pytest-dev/pytest/)
for testing.

## LICENSE

PySignature uses the Apache License 2.0.
