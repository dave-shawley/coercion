coercion
========
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

.. _tornado: http://www.tornadoweb.org/
.. _recursive_unicode: http://www.tornadoweb.org/en/stable/escape.html\
   #tornado.escape.recursive_unicode
