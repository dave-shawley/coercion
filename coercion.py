import collections
import datetime
import functools
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


def normalize_collection(coll):
    """
    Normalize all elements in a collection.

    :param coll: the collection to normalize.  This is required to
        implement one of the following protocols:
        :class:`collections.Mapping`, :class:`collections.Sequence`,
        or :class:`collections.Set`.

    :returns: a new instance of the input class with the keys and
        values normalized via :func:`.stringify`
    :raises: :exc:`RuntimeError` if `coll` is not a collection

    This function transforms the collection by recursively transforming
    each key and value contained in it.  The action is recursive but
    the implementation is unrolled and iterative.  If you are interested
    in the algorithm used, it is described as comments in the code.

    """

    #
    # The recursive version of this algorithm is something like:
    #
    #    if isinstance(coll, dict):
    #        return dict((stringify(k), normalize_collection(v))
    #                    for k, v in coll.items())
    #    if isinstance(obj, (list, tuple)):
    #        return [normalize_collection(item) for item in obj]
    #    raise RuntimeError('non-container root')
    #
    # Since this is NOT simply a tail-recursive function, unrolling
    # the recursion requires that we store intermediate "frame info"
    # somewhere while processing.  I chose to use two stacks for
    # this:
    #
    #  value_stack: contains the produced values.  The while loop
    #    appends a new container to this stack when it encounters a
    #    container on the work stack.  When the algorithm terminates,
    #    we return the first (oldest) value on the stack.
    #  work_stack: contains the items that need to be processed and
    #    a function to call when the value is completed.  Initially,
    #    we place the input collection onto work stack without a
    #    processing function.
    #
    # The algorithm starts with the input collection on the work
    # stack.  Each iteration pops the top of the stack which contains
    # a value and a completion function (inserter).  If the value is
    # a collection, then we push a new container onto the value stack,
    # iterate over the container, and push each item onto the work
    # stack with a function that will insert it into the new container.
    #

    value_stack = []
    work_stack = [(coll, None)]

    def create_container(container_type, inserter):
        clone = container_type()
        if inserter:
            inserter(clone)
        value_stack.append(clone)
        return clone

    while work_stack:
        value, inserter = work_stack.pop()
        if isinstance(value, (list, tuple)):
            target = create_container(list, inserter)
            inserter = functools.partial(target.insert, 0)
            for item in value:
                work_stack.append((item, inserter))
        elif isinstance(value, dict):
            target = create_container(dict, inserter)
            for key, item in value.items():
                inserter = functools.partial(target.__setitem__,
                                             stringify(key))
                work_stack.append((item, inserter))
        else:
            if inserter is None:
                raise RuntimeError(
                    'non-container root - type %r' % value.__class__)
            inserter(stringify(value))

    return value_stack[0]
