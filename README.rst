coercion
========
|Version| |ReadTheDocs| |TravisCI| |CodeCov|

This library provides functions that coerce datastructures into
normalized forms.  For example, converting an arbitrary ``dict``
into a form that is suitable for passing to ``json.dumps``.

The `tornado`_ framework has a function called `recursive_unicode`_
in the ``tornado.escape`` module.  It is a very simple recursive
walk of datastructure that switches on type and transforms string
values into unicode strings.  I use this in production software
regularly and it works like a charm.  Or at least it did until my
software encountered a deeply nested dictionary and I received a
``RuntimeError: maximum recursion depth exceeded`` error in my
service log.  This is one of the exceptions that strikes fear into
most engineers when it rears it's head in production.

That is the primary reason for this library existing.  It provides
the same simple string encoding function iteratively instead of
recursively.  At the same time, the need to coerce values into a
normalized string form is something that I've had to do repeatedly
so it might as well be plopped into a reusable library.

Examples
--------
The following example shows one of the underlying reasons that this
library was created.  The commonly used msgpack implementation for
python returns everything as byte strings which is problematic if
you want to dump it as JSON since it will raise a ``TypeError`` if
dictionary keys are not strings.  (This is where `recursive_unicode`_
was so handy.)

.. code-block:: python

   >>> import json
   >>> import coercion
   >>> import msgpack
   >>> bin_msg = msgpack.packb({u'\u00DCnicode': b'bytes', b'bytes': 'str'})
   >>> decoded = msgpack.unpackb(bin_msg)
   >>> decoded
   {b'bytes': b'str', b'\xc3\x9cnicode': b'bytes'}
   >>> json.dumps(decoded)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/daveshawley/opt/lib/python3.5/json/__init__.py", line 230, in dumps
       return _default_encoder.encode(obj)
     File "/Users/daveshawley/opt/lib/python3.5/json/encoder.py", line 199, in encode
       chunks = self.iterencode(o, _one_shot=True)
     File "/Users/daveshawley/opt/lib/python3.5/json/encoder.py", line 257, in iterencode
       return _iterencode(o, 0)
   TypeError: keys must be a string
   >>> json.dumps(coercion.normalize_collection(decoded))
   '{"bytes": "str", "\\u00dcnicode": "bytes"}'


.. _tornado: http://www.tornadoweb.org/
.. _recursive_unicode: http://www.tornadoweb.org/en/stable/escape.html
   #tornado.escape.recursive_unicode

.. |Version| image:: https://img.shields.io/pypi/v/coercion.svg
   :target: https://pypi.python.org/pypi/coercion
   :alt: [PyPI]
.. |ReadTheDocs| image:: https://readthedocs.org/projects/coercion/badge/
   ?version=latest
   :target: https://coercion.readthedocs.org/
   :alt: [Documentation]
.. |TravisCI| image:: https://travis-ci.org/dave-shawley/coercion.svg
   ?branch=master
   :target: https://travis-ci.org/dave-shawley/coercion
   :alt: [Build Status]
.. |CodeCov| image:: https://codecov.io/github/dave-shawley/coercion/
   coverage.svg?branch=master
   :target: https://codecov.io/github/dave-shawley/coercion?branch=master
   :alt: [Test Coverage]
