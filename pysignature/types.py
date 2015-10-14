"""Encapsulate the logic of more complex
types than the defaults provided by python,
as callables denominated **type assertions**.

The module also provides the logic for using
said type assertions.
"""
from abc import ABCMeta
from inspect import isclass
from pysignature.exceptions import PySignatureError, TypeAssertionError

def assert_type(value, assertion):
    """Main function for asserting
    if a given value succeeds on
    an assertion function.
    Returns None if succeeds, otherwise
    raise a PySignatureError."""
    try:
        if isclass(assertion) and issubclass(assertion, TypeAssertion):
            assertion_instance = assertion()
            assertion_instance.assertion(value)
        elif callable(getattr(assertion, 'assertion', None)):
            assertion.assertion(value)
        else:
            assertion(value)
        return None
    except ValueError:
        raise TypeAssertionError(assertion.__name__, value)

class TypeAssertion(object):
    """Base abstract class for defining type assertions."""
    __metaclass___ = ABCMeta
    def assertion(self, *args):
        raise NotImplementedError

    def __repr__(self):
        return self.__class__.__name__

class ParametrizedTypeAssertion(TypeAssertion):
    """Base abstract classe for creating
    assertions that are supposed to be
    instantiated with different arguments.
    """
    __metaclass__ = ABCMeta
    def __init__(self, *args, **kwargs):
        self.parameters = args
        self.options = kwargs

    def __repr__(self):
        cls = self.__class__.__name__
        reprs = []
        for param in self.parameters:
            if isinstance(param, TypeAssertion):
                reprs.append(repr(param))
            else:
                reprs.append(param.__name__)
        return cls + '(' + ', '.join(reprs) + ')'


class Any(TypeAssertion):
    """Assertion that passes on any value."""
    def assertion(self, value):
        pass

class String(TypeAssertion):
    """Assertion for string objects."""
    def assertion(self, value):
        if not isinstance(value, basestring):
            raise TypeAssertionError(self, value)

class Or(ParametrizedTypeAssertion):
    """Parametrized assertion that only fails if
    the last of the given assertions does not pass.
    """
    def assertion(self, value):
        for param in self.parameters:
            try:
                assert_type(value, param)
                break
            except TypeAssertionError:
                pass
            except ValueError:
                pass
        else:
            raise TypeAssertionError(self, value)

class Tuple(ParametrizedTypeAssertion):
    """Assertion that verifies that a tuple
    contains the structure specified
    in the given parameters.
    """
    def assertion(self, value):
        if not isinstance(value, tuple):
            raise TypeAssertionError(self, value)
        if not(len(value) == len(self.parameters)):
            raise TypeAssertionError(self, value)
        for item, param in zip(value, self.parameters):
            try:
                assert_type(item, param)
            except TypeAssertionError:
                raise TypeAssertionError(self, value)

class List(ParametrizedTypeAssertion):
    """Assertion that verifies that the value
    is a list in which all of the elements
    pass the type assertion (given in the parameter).
    """
    def assertion(self, value):
        if not isinstance(value, list):
            raise TypeAssertionError(self, value)

        type_assertion = self.parameters[0]
        for item in value:
            try:
                assert_type(item, type_assertion)
            except TypeAssertionError:
                raise TypeAssertionError(self, value)


class InstanceOf(ParametrizedTypeAssertion):
    """Parametrized assertion that receives
    a base class so that when de assertion
    method is run, it is checked if the value
    is an instance of the given class.
    """
    def assertion(self, value):
        cls = self.parameters[0]
        if not (isclass(cls) and isinstance(value, cls)):
            raise TypeAssertionError(self, value)

class Set(ParametrizedTypeAssertion):
    """Parametrized type assertion
    that verifies that the given value
    is a set and every element is of the
    specified type assertion.
    """
    def assertion(self, value):
        t_assert = self.parameters[0]
        if not isinstance(value, set):
            raise TypeAssertionError(self, value)
        for item in value:
            try:
                assert_type(item, t_assert)
            except TypeAssertionError:
                raise TypeAssertionError(self, value)

class Dictionary(ParametrizedTypeAssertion):
    """Parametrized type assertion for a fixed type
    dictionary in which both the keys and the types
    must agree to their specified type assertions.
    """
    def assertion(self, value):
        k_assert = self.parameters[0]
        v_assert = self.parameters[1]
        for key, val in value.iteritems():
            try:
                assert_type(key, k_assert)
                assert_type(val, v_assert)
            except:
                raise TypeAssertionError(self, value)

class Boolean(TypeAssertion):
    """Assertion for verifying that
    the given parameter is a boolean value.
    """
    def assertion(self, value):
        if not isinstance(value, bool):
            raise TypeAssertionError(self, value)

class Numeric(TypeAssertion):
    """Assertion for validating that
    the given value is either an
    integer or a float.
    """
    def assertion(self, value):
        try:
            assert_type(value, Or(int, float))
        except TypeAssertionError:
            raise TypeAssertionError(self, value)
