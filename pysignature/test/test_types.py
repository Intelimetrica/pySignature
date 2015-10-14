import pytest

from pysignature import exceptions
from pysignature.types import (
    Any, String, Or, Tuple, List, InstanceOf, Set,
    Dictionary, Boolean, Numeric, assert_type
)

def test_fail_basic_type_assertion():
    with pytest.raises(exceptions.PySignatureError):
        assert_type('hello', int)

def test_correct_assertion_returns_none():
    assert assert_type(5, int) is None

def test_passes_for_any_type_assertion():
    assert assert_type(5, Any) is None
    assert assert_type('str', Any) is None
    assert assert_type(lambda x: x, Any) is None
    assert assert_type(pytest, Any) is None

def test_string_type_assertion_success():
    assert assert_type('hi', String) is None
    assert assert_type(u'hi', String) is None

def test_string_type_assertion_error():
    with pytest.raises(exceptions.TypeAssertionError) as error:
        assert_type(5, String)
    assert "'5' is not a String" in str(error)

def test_or_assertion_success():
    assert assert_type(5, Or(float, int)) is None
    assert assert_type('hi', Or(int, String)) is None
    assert assert_type('hi', Or(float, int, String)) is None

def test_or_assertion_short_circuit():
    def failure():
        raise Exception
    assert assert_type(1, Or(int, failure)) is None

def test_or_assertion_failure():
    with pytest.raises(exceptions.TypeAssertionError) as error:
        assert_type('hi', Or(int, float))
    assert "'hi' is not a Or(int, float)" in str(error)

def test_tuple_assertion_success():
    assert assert_type((1, 2, 3), Tuple(int, int, int)) is None
    assert assert_type(('a', 1, object()), Tuple(String, int, Any)) is None
    assert assert_type((), Tuple()) is None
    assert assert_type((1, ('a', 'b')), Tuple(int, Tuple(String, String))) is None

def test_tuple_assertion_failure_for_non_tuples():
    with pytest.raises(exceptions.TypeAssertionError) as error:
        assert_type(1, Tuple())
    assert "'1' is not a Tuple()" in str(error)

def test_tuple_assertion_failure_for_different_lengths():
    with pytest.raises(exceptions.TypeAssertionError) as error1:
        assert_type((1, 2, 3), Tuple(int, int))
    assert "'(1, 2, 3)' is not a Tuple(int, int)" in str(error1)

    with pytest.raises(exceptions.TypeAssertionError) as error2:
        assert_type((1, 2, 3), Tuple(int, int, int, int))
    assert "'(1, 2, 3)' is not a Tuple(int, int, int, int)"


def test_tuple_assertion_failure_wrong_types():
    with pytest.raises(exceptions.TypeAssertionError) as error:
        assert_type((1, 'a'), Tuple(int, int))
    assert "'(1, 'a')' is not a Tuple(int, int)" in str(error)

def test_list_assertion_success():
    assert assert_type([1, 2, 4.5], List(Or(float, int))) is None
    assert assert_type([['a'], ['v', 'c'], []], List(List(String))) is None

def test_list_assertion_failure():
    with pytest.raises(exceptions.TypeAssertionError) as error1:
        assert_type([1, 2, 3], List(String))
    assert "'[1, 2, 3]' is not a List(String)" in str(error1)

    with pytest.raises(exceptions.TypeAssertionError) as error2:
        assert_type([[[1], [2, 3]], [[4], 5], [[6]]], List(List(List(int))))
    assert "'[[[1], [2, 3]], [[4], 5], [[6]]]' is not a List(List(List(int)))" in str(error2)

def test_instanceof_assertion_success():
    class X:
        pass
    class Y(X):
        pass
    assert assert_type(X(), InstanceOf(X)) is None
    assert assert_type(Y(), InstanceOf(X)) is None

def test_instance_assertion_error():
    class X:
        pass
    with pytest.raises(exceptions.TypeAssertionError) as error:
        assert_type(1, InstanceOf(X))
    assert "'1' is not a InstanceOf(X)" in str(error)

def test_boolean_assertion_success():
    assert assert_type(True, Boolean) is None
    assert assert_type(False, Boolean) is None

def test_boolean_assertion_failure():
    with pytest.raises(exceptions.TypeAssertionError) as error:
        assert_type(1, Boolean)
    assert "'1' is not a Boolean" in str(error)

def test_set_assertion_success():
    assert assert_type({1, 2}, Set(int)) is None
    assert assert_type({'a', 1}, Set(Or(String, int))) is None

def test_set_assertion_failure():
    with pytest.raises(exceptions.TypeAssertionError) as error1:
        assert_type([1, 2], Set(int))
    assert "'[1, 2]' is not a Set(int)" in str(error1)

    with pytest.raises(exceptions.TypeAssertionError) as error2:
        assert_type({1, 2}, Set(String))
    assert "'set([1, 2])' is not a Set(String)" in str(error2)

def test_dictionary_assertion_success():
    assert assert_type({'a': 1, 'b': 2}, Dictionary(String, int)) is None
    assert assert_type({1: 'a', 2: 2}, Dictionary(int, Or(String, int))) is None

def test_numeric_assertion_success():
    assert assert_type(1, Numeric) is None
    assert assert_type(-1.0, Numeric) is None

def test_numeric_assertion_failure():
    with pytest.raises(exceptions.PySignatureError) as error:
        assert_type('a', Numeric)
    assert "'a' is not a Numeric" in str(error)
