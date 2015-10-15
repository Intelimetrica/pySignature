"""Definitions of pysignature
exception classes.

All exceptions of this project
inherit from the main PySignatureError
exception class.
"""

class PySignatureError(Exception):
    """Main exception for the PySignature project."""
    pass

class TypeAssertionError(PySignatureError, AssertionError):
    """Assertion for specifying a failed type assertion."""
    def __init__(self, assertion, target):
        message = "Type assertion failed: '%s' is not a %s" % (target, repr(assertion))
        super(TypeAssertionError, self).__init__(message)

class BadTypeSpecError(PySignatureError):
    """Exception that represents that the type signature was
    inconsistently formed."""
    pass

class FunctionTypeCheckError(PySignatureError):
    """Exception that represents a failure to typecheck
    the call to a function.
    """
    def __init__(self, fn, errors):
        name = fn.__name__
        amount = len(errors)
        self.errors = errors
        message = "Failed to typecheck function '%s': error in %i argument(s)" % (name, amount)
        super(FunctionTypeCheckError, self).__init__(message)
