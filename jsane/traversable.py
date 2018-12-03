class JSaneException(Exception):
    pass


class Empty(object):
    def __init__(self, key_name=""):
        self._key_name = key_name

    def __getattr__(self, key):
        return self
    __getitem__ = __getattr__

    def __repr__(self):
        return "<Traversable key does not exist: %s>" % self._key_name

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
                    "Unexpected argument: %s" % (next(iter(kwargs)),)
                )
            return default
        else:
            raise JSaneException("Key does not exist: %s" % (self._key_name,))
    __call__ = r


class Traversable(object):
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, key):
        try:
            return Traversable(self._obj[key])
        except (KeyError, AttributeError, IndexError, TypeError):
            return Empty(key)
    __getitem__ = __getattr__

    def __eq__(self, other):
        """Equality test."""
        if not hasattr(other, "_obj"):
            return False
        return self._obj == other._obj

    def __repr__(self):
        return "<Traversable: %r>" % self._obj

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
            raise TypeError("Unexpected argument: %s" % (next(iter(kwargs)),))
        return self._obj
    __call__ = r
