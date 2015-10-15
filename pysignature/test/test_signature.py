import pytest

from pysignature import exceptions
from pysignature import typechecked
from pysignature.types import (
    Any, String, Or, Tuple, List, InstanceOf, Set,
    Dictionary, Boolean, Numeric
)

# Decorated functions
@typechecked(a=int, b=int, c=String)
def x(a, b, c):
    return c + str(a + b)

@typechecked(a=int, _variadic=String)
def y(a, *args):
    return str(a) + ','.join(args)

@typechecked(a=String, _named=Numeric)
def z(a, **kwargs):
    return a + str(sum(kwargs.values()))

@typechecked(a=String, b=Numeric)
def w(a, b=1):
    return a + ':' + str(b)

def test_typechecked_decorator_basic_use_does_not_interfere_with_function():
    assert x(1, 2, 'c') == 'c3'

def test_typechecked_decorator_with_default_values_success():
    assert w('a') == 'a:1'

def test_typechecked_decorator_basic_failure():
    with pytest.raises(exceptions.FunctionTypeCheckError) as error:
        x(1, 'a', 'b')
    assert "Failed to typecheck function 'x': error in 1 argument(s)" in str(error)
    assert len(error.value.errors) == 1
    assert error.value.errors[0].arg == 'b'
    assert "'a' is not a 'int'" in error.value.errors[0].error

def test_typechecked_decorator_multiple_arg_failure():
    with pytest.raises(exceptions.FunctionTypeCheckError) as error:
        x('a', 'b', 1)
    assert "Failed to typecheck function 'x': error in 3 argument(s)" in str(error)
    errors = error.value.errors
    assert len(errors) == 3
    assert {'a', 'b', 'c'} == set(err.arg for err in errors)

def test_typechecked_decorator_variadic_arguments_success():
    assert y(1, 'a', 'b') == '1a,b'

def test_typechecked_decorator_variadic_arguments_failure():
    with pytest.raises(exceptions.FunctionTypeCheckError) as error:
        y(1, 'a', 3)
    exception = error.value
    assert "Failed to typecheck function 'y': error in 1 argument(s)" == str(exception)
    assert exception.errors[0].arg == 'Variadic argument 1'
    assert "'3' is not a String" in exception.errors[0].error

def test_typechecked_decorator_with_keyword_arguments_success():
    assert z('a', b=1, c=2, d=3) == 'a6'

def test_typechecked_decorator_with_keyword_arguments_failure():
    with pytest.raises(exceptions.FunctionTypeCheckError) as error:
        z('a', b=1, c='w')
    exception = error.value
    assert "Failed to typecheck function 'z': error in 1 argument(s)" == str(exception)
    assert exception.errors[0].arg == "Keyword argument 'c'"
    assert "'w' is not a Numeric" in exception.errors[0].error

def test_typespec_validation_error_missing_varargs():
    with pytest.raises(exceptions.BadTypeSpecError) as error:
        @typechecked(a=int)
        def tmp(a, *args):
            pass
    assert 'No type specified for variadic arguments' in str(error)

def test_typespec_validation_error_unsupported_varargs():
    with pytest.raises(exceptions.BadTypeSpecError) as error:
        @typechecked(a=int, _variadic=int)
        def tmp(a):
            pass
    assert 'Function does not support variadic arguments' in str(error)

def test_typespec_validation_error_missing_kwargs():
    with pytest.raises(exceptions.BadTypeSpecError) as error:
        @typechecked(a=int)
        def tmp(a, **kwargs):
            pass
    assert 'No type specified for keyword arguments' in str(error)

def test_typespec_validation_error_unsupported_kwargs():
    with pytest.raises(exceptions.BadTypeSpecError) as error:
        @typechecked(a=int, _named=int)
        def tmp(a):
            pass
    assert 'Function does not support keyword arguments' in str(error)

def test_wrapped_function_can_have_its_typechecking_bypassed():
    assert x.untyped('a', 'b', 'c') == 'cab'

def test_wrapped_function_throws_an_error_when_wrong_number_of_arguments():
    with pytest.raises(TypeError) as error:
        x()
    assert str(error.value) == "x() takes exactly 3 arguments (0 given)"
