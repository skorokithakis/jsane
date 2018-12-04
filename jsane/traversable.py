from numbers import Number


class JSaneException(KeyError):
    pass


class Empty(object):
    def __init__(self, key_name=""):
        self._key_name = key_name

    def __getattr__(self, _):
        return self  # Empty object returned should reflect the 1st failed key
    __getitem__ = __getattr__

    def __setattr__(self, key, value):
        if key == '_key_name':
            return object.__setattr__(self, '_key_name', value)
        raise JSaneException("There is nothing here!")

    def __delattr__(self, key):
        raise JSaneException(
            "Key does not exist: {}".format(repr(self._key_name))
        )
    __delitem__ = __delattr__

    def __eq__(self, other):
        return False

    def __repr__(self):
        return "<Traversable key does not exist: {}>".format(
            repr(self._key_name)
        )

    def r(self, **kwargs):
        """
        Resolve the object.

        This returns default (if present) or fails on an Empty.
        """
        # by using kwargs we ensure that usage of positional arguments, as if
        # this object were another kind of function, will fail-fast and raise
        # a TypeError
        if 'default' in kwargs:
            default = kwargs.pop('default')
            if kwargs:
                raise TypeError(
                    "Unexpected argument: {}".format(repr(next(iter(kwargs))))
                )
            return default
        else:
            raise JSaneException(
                "Key does not exist: {}".format(repr(self._key_name))
            )
    __call__ = r

    def __pos__(self):
        return float('nan')

    def __str__(self):
        raise JSaneException(
            "Key does not exist: {}".format(repr(self._key_name))
        )
    __int__ = __float__ = __str__

    def __contains__(self, _):
        return False

    def __dir__(self):
        raise JSaneException(
            "Key does not exist: {}".format(repr(self._key_name))
        )


class Traversable(object):
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, key):
        try:
            return Traversable(self._obj[key])
        except (KeyError, AttributeError, IndexError, TypeError):
            return Empty(key)
    __getitem__ = __getattr__

    def __setattr__(self, key, value):
        if key == '_obj':
            object.__setattr__(self, '_obj', value)
            return
        if isinstance(value, Traversable):
            value = value._obj
        # may cause TypeError; allow this to fall through
        self._obj[key] = value

    def __setitem__(self, key, value):
        if isinstance(value, Traversable):
            value = value._obj
        # may cause TypeError; allow this to fall through
        self._obj[key] = value

    def __delattr__(self, key):
        try:
            del self._obj[key]
        except KeyError:
            raise JSaneException("Key does not exist: {}".format(repr(key)))
    __delitem__ = __delattr__

    def __eq__(self, other):
        """
        Compare to other objects very reluctantly.

        Only succeed when both objects are Traversable objects, and
        fail otherwise (which defaults to returning False) to ensure
        that the developer doesn't forget too easily what kind of
        object they're actually using.
        """
        if isinstance(other, Traversable):
            return self._obj == other._obj
        else:
            return NotImplemented

    def __repr__(self):
        return "<Traversable: {}>".format(repr(self._obj))

    def r(self, **kwargs):
        """
        Resolve the object.

        This will always succeed, since, if a lookup fails, an Empty
        instance will be returned farther upstream.
        """
        # by using kwargs we ensure that usage of positional arguments, as if
        # this object were another kind of function, will fail-fast and raise
        # a TypeError
        kwargs.pop('default', None)
        if kwargs:
            raise TypeError(
                "Unexpected argument: {}".format(repr(next(iter(kwargs))))
            )
        return self._obj
    __call__ = r

    def __pos__(self):
        """
        Resolve the object as a number ONLY if it is a number.

        Missing keys or non-numeric type will yield nan. Numeric
        strings are not considered to be numbers under this
        determination.
        """
        if isinstance(self._obj, Number):
            return self._obj
        else:
            return float('nan')

    def __str__(self):
        """
        Resolve the object and turn it into a string if it is not already.

        Essentially, str(traversable) is syntactic sugar for
        str(traversable()).
        """
        return str(self._obj)

    def __int__(self):
        """
        Resolve the object as an int if possible.

        Essentially, int(traversable) is syntactic sugar for
        int(traversable()).
        """
        return int(self._obj)

    def __float__(self):
        """
        Resolve the object as a float if possible.

        Essentially, float(traversable) is syntactic sugar for
        float(traversable()).
        """
        return float(self._obj)

    def __contains__(self, key):
        """
        Test for containment if the wrapped object is a list or dict.

        Do not always check for containment whenever it supports the
        operator, as this could result in some very sneaky bugs if a
        key in the JSON is a string instead of a nested JSON object.
        """
        if isinstance(self._obj, (dict, list)):
            return key in self._obj
        else:
            return False

    def __dir__(self):
        """
        Return the attributes of this object.

        Includes keys of the internal object if it's a dictionary.
        Tremendously helpful for advanced interactive shell.
        """
        keys = dir(super(Traversable, self))
        if isinstance(self._obj, dict):
            keys += sorted(str(k) for k in self._obj)
        return keys
