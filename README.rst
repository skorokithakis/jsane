JSane
=====

.. image:: https://travis-ci.org/skorokithakis/jsane.svg?branch=master
    :target: https://travis-ci.org/skorokithakis/jsane

JSane is a JSON "parser" that makes attribute accesses easier.

Three-line intro
----------------

::

    >>> import jsane
    >>> j = jsane.loads('{"foo": {"bar": {"baz": ["well", "hello", "there"]}}}')
    >>> j.foo.bar.baz[1].r()
    'hello'


Motivation
----------

Picture the scene. You're a jet-setting developer who is obsessed with going to
the gym. One day, a world-class jewel thief kidnaps you and asks you to hack
into the super-secure bank server in thirty seconds, while an ultramodel is
performing oral sex on you. You hurriedly trace the protocol on the wire, only
to discover, to your dismay, that it uses JSON. Nested JSON, with levels and
levels of keys.

It's hopeless! You'll never type all those brackets and quotation marks in time!
Suddenly, a flash of a memory races through your mind, like some cliche from
a badly-written README. You launch the shell and type two words::

    import jsane

`The day is saved`_.


Motivation (non-Hollywood version)
----------------------------------

Are you frustrated with having to traverse your nested JSON key by key?

::

    root = my_json.get("root")
    if root is None:
        return None

    key1 = root.get("key1")
    if key1 is None:
        return None

    key2 = key1.get("key2")
    if key2 is None:
        return None

    <five more times>

Is your code ruined by pesky all-catching ``except`` blocks?

::

    try:
        my_json["root"]["key1"]["key2"]["key3"]
    except:
        return None

Are you tired of typing all the braces and quotes all the time?

::

    my_json["root"]["key1"[""]][]"]']'"}}""]

Now there's JSane!


Motivation (non-infomercial version)
------------------------------------

Okay seriously, ``this["thing"]["is"]["no"]["fun"]``. JSane lets you
``traverse.json.like.this.r()``. That's it.


Usage
-----

Using JSane is simple, at least. It's pretty much a copy of the builtin
``json`` module.

First of all, install it with ``pip`` or ``easy_install``::

    pip install jsane

Here's an example of its usage::

    >>> import jsane

    >>> j = jsane.loads('{"some": {"json": [1, 2, 3]}}')
    >>> j.some.json[2].r()
    3

You can also load an existing object::
    >>> j = jsane.from_object({"hi": "there"})
    >>> j.hi
    <Traversable: 'there'>

If the object contains any data types that aren't valid in JSON (like
functions), it still should work, but you're on your own.

Due to Python being a sensible language, there's a limit to the amount of
crap you can pull with it, so JSane actually returns a ``Traversable`` object on
accesses::

    >>> j = jsane.loads('{"foo": {"bar": {"baz": "yes!"}}}')
    >>> type(j.foo)
    <class 'jsane.traversable.Traversable'>

If you want your real object back at the end of the wild attribute ride, call
``.r()``::

    >>> j.foo.bar.r()
    {'baz': 'yes!'}

Likewise, if you prefer, you can call the object as a function with no
arguments::

    >>> j.foo.bar()
    {'baz': 'yes!'}

If an attribute, item or index along the way does not exist, you'll get an
exception. You can get rid of that by specifying a default::

    >>> import jsane

    >>> j = jsane.loads('{"some": "json"}')
    >>> j.this.path.doesnt.exist.r()
    Traceback (most recent call last):
      ...
    jsane.traversable.JSaneException: "Key does not exist: 'this'"
    >>> j.haha_sucka_this_doesnt_exist_either.r(default="💩")
    '💩'

"But how do I access a key called ``__call__``, ``r``, or ``_obj`` where you
store the wrapped object?!", I hear you ask. Worry not, object keys are still
accessible with indexing::

    >>> j = jsane.loads('{"r": {"__call__": {"_obj": 5}}}')
    >>> j["r"]["__call__"]["_obj"].r()
    5

For convenience, you can access values specifically as numbers::

    >>> import jsane

    >>> j = jsane.loads('''
    ...     {
    ...       "numbers": {
    ...         "one": 1,
    ...         "two": "2"
    ...       },
    ...       "letters": "XYZ"
    ...     }
    ... ''')
    >>> +j.numbers.one
    1
    >>> +j.letter, +j.numbers.two  # Things that aren't numbers are nan
    (nan, nan)
    >>> +j.numbers
    nan
    >>> +j.what  # Things that don't exist are also nan.
    nan

(NaN is not representable in JSON, so this should be enough for most use cases.
Testing for NaN is also easy with the standard library ``math.isnan()``
function.)

Likewise for strings, calling ``str()`` on a Traversable object is a simple
shortcut::

    >>> str(j.letters)
    'XYZ'
    >>> str(j.numbers)
    "{'one': 1, 'two': '2'}"
    >>> str(j.numbers.one)
    '1'

In the same fashion, ``int()`` and ``float()`` are also shortcuts, but unlike
``str()`` (and consistent with their behavior elsewhere in Python) they do not
infallibly return objects of their respective type (that is, they may raise a
ValueError instead).

That's about it. No guarantees of stability before version 1, as always. Semver
giveth, and semver taketh away.

Help needed/welcome/etc, mostly with designing the API. Also, if you find this
library useless, let me know.


License
-------

BSD. Or MIT. Whatever's in the LICENSE file. I forget. It's permissive, though,
so relax.


Self-promotion
--------------

It's me, Stavros.


FAQ
---

* Do you find it ironic that the README for JSane is insane?

  No.

* Is this library awesome?

  Yes.

* All my JSON data uses 'r' and '_obj' as keys!

  Come on, man. :(

.. _The day is saved: https://www.youtube.com/watch?v=mWqGJ613M5Y
