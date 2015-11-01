import datetime
import sys
import uuid


version_info = (0, 0, 0)
"""Library version as an ordered tuple of integers."""

__version__ = '.'.join(str(c) for c in version_info)
"""Human-readable library version."""


def stringify(obj):
    """
    Return the string representation of an object.

    :param obj: object to get the representation of
    :returns: unicode string representation of `obj` or `obj` unchanged

    This function returns a string representation for many of the
    types from the standard library.  It does not convert numeric or
    Boolean values to strings -- it only converts non-primitive instances
    such as :class:`datetime.datetime`.  The following table describes
    the types that are handled and describes how they are represented.

    +----------------------------+--------------------------------------------+
    | Class                      | Behavior                                   |
    +============================+============================================+
    | :class:`uuid.UUID`         | ``str(obj)``                               |
    +----------------------------+--------------------------------------------+
    | :class:`datetime.datetime` | ``obj.strftime('%Y-%m-%dT%H:%M:%S.%f%z')`` |
    +----------------------------+--------------------------------------------+
    | :class:`memoryview`        | ``obj.tobytes().decode('utf-8')``          |
    +----------------------------+--------------------------------------------+
    | :class:`bytearray`         | ``bytes(obj).decode('utf-8')``             |
    +----------------------------+--------------------------------------------+
    | :class:`buffer`            | ``bytes(obj).decode('utf-8')``             |
    +----------------------------+--------------------------------------------+
    | :class:`bytes`             | ``obj.decode('utf-8')``                    |
    +----------------------------+--------------------------------------------+

    Other types are returned unharmed.

    """
    out = obj
    if isinstance(obj, uuid.UUID):
        out = str(obj)
    elif hasattr(obj, 'strftime'):
        out = obj.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    elif isinstance(obj, memoryview):
        out = obj.tobytes()
    elif isinstance(obj, bytearray):
        out = bytes(obj)
    elif sys.version_info[0] < 3 and isinstance(obj, buffer):
        out = bytes(obj)

    if isinstance(out, bytes):
        out = out.decode('utf-8')

    return out
