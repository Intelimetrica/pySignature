"""Logic for creating function signatures."""

import functools
import inspect
from collections import namedtuple
from pysignature.exceptions import (
    BadTypeSpecError, TypeAssertionError,
    FunctionTypeCheckError
)
import pysignature.types as t

class Signature(object):
    """Encapsulate the logic of handling
    a signature through instances of this
    class.
    """
    def __init__(self, fn, type_spec):
        """Given a type_spec dictionary and
        a target function, create the
        Signature object.
        """
        argspec = inspect.getargspec(fn)
        self.varargs_name = argspec.varargs
        self.kwargs_name = argspec.keywords
        self.type_spec = type_spec
        self.fn = fn
        self.validate_spec()

    def validate_spec(self):
        """Verify that the given typespec
        is consistent with the function
        argument definition.
        """
        specifies_variadic = self.type_spec.has_key('_variadic')
        specifies_named = self.type_spec.has_key('_named')
        if (self.varargs_name is not None) and not specifies_variadic:
            raise BadTypeSpecError('No type specified for variadic arguments')
        elif (self.varargs_name is None) and specifies_variadic:
            raise BadTypeSpecError('Function does not support variadic arguments')
        elif (self.kwargs_name is not None) and not specifies_named:
            raise BadTypeSpecError('No type specified for keyword arguments')
        elif (self.kwargs_name is None) and specifies_named:
            raise BadTypeSpecError('Function does not support keyword arguments')

    def typecheck(self, *args, **kwargs):
        """Use the original type specification
        for validating the given types.
        """
        callargs = inspect.getcallargs(self.fn, *args, **kwargs)
        errors = []
        for arg, value in callargs.iteritems():
            if arg == self.varargs_name:
                errors.extend(self._typecheck_varargs(arg, value))
            elif arg == self.kwargs_name:
                errors.extend(self._typecheck_kwargs(arg, value))
            else:
                try:
                    t.assert_type(value, self.type_spec[arg])
                except TypeAssertionError as e:
                    errors.append(TypeArgumentError(arg, str(e)))
        if len(errors) > 0:
            raise FunctionTypeCheckError(self.fn, errors)

    def _typecheck_varargs(self, arg, value):
        errors = []

        for idx, item in enumerate(value):
            try:
                t.assert_type(item, self.type_spec['_variadic'])
            except TypeAssertionError as e:
                msg = 'Variadic argument %i' % idx
                errors.append(TypeArgumentError(msg, str(e)))

        return errors

    def _typecheck_kwargs(self, arg, value):
        errors = []

        for key, item in value.iteritems():
            try:
                t.assert_type(item, self.type_spec['_named'])
            except TypeAssertionError as e:
                msg = "Keyword argument '%s'" % key
                errors.append(TypeArgumentError(msg, str(e)))

        return errors

TypeArgumentError = namedtuple('TypeArgumentError', ['arg', 'error'])

def typechecked(**kwargs):
    """Returns a decorator for typechecking functions.

    Given its keyword arguments, creates a Signature
    and a wrapped function that verifies that its
    arguments typecheck. It also adds a property to
    such wrapper, 'untyped', for bypassing the typechecking.

    The arguments must use the same names as the wrapped
    function arguments. If variadic or keyword arguments
    are used, extra arguments must be passed to this
    function: '_variadic' and '_named', respectively. A single
    TypeAssertion is given to these especial arguments,
    and each one of their members must pass such assertion.
    """
    def typecheck_decorator(fn):
        signature = Signature(fn, kwargs)
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            signature.typecheck(*args, **kwargs)
            return fn(*args, **kwargs)
        decorated.untyped = fn
        return decorated
    return typecheck_decorator
