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
    return Traversable(jdict)
