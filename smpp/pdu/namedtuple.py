"""
This file comes from http://code.activestate.com/recipes/500261-named-tuples/
Licensed under Python Software Foundation license: http://www.opensource.org/licenses/PythonSoftFoundation

"""

from operator import itemgetter as _itemgetter
from keyword import iskeyword as _iskeyword
import sys as _sys

#pylint: disable-msg=E0102
def namedtuple(typename, field_names, verbose=False, rename=False):
    """Returns a new subclass of tuple with named fields.

    >>> Point = namedtuple('Point', 'x y')
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1]                     # indexable like a plain tuple
    33
    >>> x, y = p                        # unpack like a regular tuple
    >>> x, y
    (11, 22)
    >>> p.x + p.y                       # fields also accessable by name
    33
    >>> d = p._asdict()                 # convert to a dictionary
    >>> d['x']
    11
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22)
    >>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
    Point(x=100, y=22)

    """

    # Parse and validate the field names.  Validation serves two purposes,
    # generating informative error messages and preventing template injection attacks.
    if isinstance(field_names, str):
        field_names = field_names.replace(',', ' ').split() # names separated by whitespace and/or commas
    field_names = tuple(map(str, field_names))
    if rename:
        names = list(field_names)
        seen = set()
        for i, name in enumerate(names):
            if (not min(c.isalnum() or c=='_' for c in name) or _iskeyword(name)
                or not name or name[0].isdigit() or name.startswith('_')
                or name in seen):
                    names[i] = '_%d' % i
            seen.add(name)
        field_names = tuple(names)
    for name in (typename,) + field_names:
        if not min(c.isalnum() or c=='_' for c in name):
            raise ValueError('Type names and field names can only contain alphanumeric characters and underscores: %r' % name)
        if _iskeyword(name):
            raise ValueError('Type names and field names cannot be a keyword: %r' % name)
        if name[0].isdigit():
            raise ValueError('Type names and field names cannot start with a number: %r' % name)
    seen_names = set()
    for name in field_names:
        if name.startswith('_') and not rename:
            raise ValueError('Field names cannot start with an underscore: %r' % name)
        if name in seen_names:
            raise ValueError('Encountered duplicate field name: %r' % name)
        seen_names.add(name)

    namespace = dict(
        _itemgetter=_itemgetter,
        __name__='namedtuple_%s' % typename,
        _property=property,
        _tuple=tuple
    )

    try:
        result = create_namedtuple(typename=typename, field_names=field_names)
    except SyntaxError as e:
        raise SyntaxError(e.message)

    return result

def create_namedtuple(typename, field_names):
    def _make(self, iterable):
        result = tuple.__new__(self, iterable)
        if len(result) != len(self._fields):
            raise TypeError(f"Expected {len(self._fields)} arguments, got {len(result)}")
        return result
    
    def _asdict(self):
        return dict(zip(self._fields, self))
    
    def _replace(self, **kwds):
        updated_fields = [kwds.pop(name, getattr(self, name)) for name in self._fields]
        if kwds:
            raise ValueError(f"Got unexpected field names: {kwds.keys()}")
        return self._make(updated_fields)
    
    class_dict = {
        '__slots__': (),
        '_fields': field_names,
        '__new__': _make,
        '_make': classmethod(_make),
        '_asdict': _asdict,
        '_replace': _replace,
        '__getnewargs__': lambda self: tuple(self),
        '__repr__': lambda self: f"{typename}({', '.join(map(repr, self))})",
        '__module__': _sys._getframe(1).f_globals.get('__name__', '__main__')
    }

    for i, name in enumerate(field_names):
        class_dict[name] = property(_itemgetter(i))
    
    return class_dict




if __name__ == '__main__':
    # verify that instances can be pickled
    from pickle import loads, dumps
    Point = namedtuple('Point', 'x, y', True)
    p = Point(x=10, y=20)
    assert p == loads(dumps(p, -1))

    # test and demonstrate ability to override methods
    class Point(namedtuple('Point', 'x y')):
        @property
        def hypot(self):
            return (self.x ** 2 + self.y ** 2) ** 0.5
        def __str__(self):
            return 'Point: x=%6.3f y=%6.3f hypot=%6.3f' % (self.x, self.y, self.hypot)

    class Point(namedtuple('Point', 'x y')):
        'Point class with optimized _make() and _replace() without error-checking'
        _make = classmethod(tuple.__new__)
        def _replace(self, _map=map, **kwds):
            return self._make(_map(kwds.get, ('x', 'y'), self))

    import doctest
    TestResults = namedtuple('TestResults', 'failed attempted')

