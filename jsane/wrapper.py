import json

from .traversable import Traversable


def load(*args, **kwargs):
    j = json.load(*args, **kwargs)
    return Traversable(j)


def loads(*args, **kwargs):
    j = json.loads(*args, **kwargs)
    return Traversable(j)


def dump(*args, **kwargs):
    return json.dump(*args, **kwargs)


def dumps(*args, **kwargs):
    return json.dumps(*args, **kwargs)


def from_dict(jdict):
    """
    Return a JSane Traversable object from a dict.
    """
    return Traversable(jdict)


def from_object(obj):
    """
    Return a JSane Traversable object from any object (e.g. a list).
    """
    return Traversable(obj)
