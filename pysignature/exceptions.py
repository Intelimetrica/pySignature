"""Definitions of pysignature
exception classes.

All exceptions of this project
inherit from the main PySignatureError
exception class.
"""

class PySignatureError(Exception):
    """Main exception for the PySignature project."""
    pass

class TypeAssertionError(PySignatureError):
    """Assertion for specifying a failed type assertion."""
    def __init__(self, assertion, target):
        message = "Type assertion failed: '%s' is not a %s" % (target, repr(assertion))
        super(TypeAssertionError, self).__init__(message)
