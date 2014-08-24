#!/usr/bin/env python
# -*- coding: utf-8 -*-

__docformat__ = "restructuredtext en"

import inspect
import uuid
import pprint

##############################################################################
##############################################################################
### Helper classes
##############################################################################
##############################################################################


class _parameter_decorator(object):
    """
    This class adds a documentation string to the annotations of a function or
    class instance's parameter.  You can add multiple documentation strings,
    or you can add one at a time.  Note that it is intended to only be used by
    the annotizer class.
    """
    def __init__(self, ID, *args, **kwargs):
        self._ID = ID
        self._args = args
        self._kwargs = kwargs
    # End of __init__()

    def __call__(self, f):
        sig = inspect.signature(f)

        func_args = {x for x in sig.parameters}
        decorator_args = {x for x in self._kwargs}
        keys = func_args.intersection(decorator_args)

        for key in keys:
            if key not in f.__annotations__:
                f.__annotations__[key] = dict()
            if self._ID not in f.__annotations__[key]:
                f.__annotations__[key][self._ID] = dict()
            f.__annotations__[key][self._ID]["doc"] = self._kwargs[key]

        return f
    # End of __call__()
# End of class _parameter_decorator

class _return_decorator(object):
    """
    This class adds a documentation string to the annotations of a function or
    class instance's return value.
    """
    def __init__(self, ID, *args, **kwargs):
        self._ID = ID
        self._args = args
        self._kwargs = kwargs
    # End of __init__()

    def __call__(self, f):
        sig = inspect.signature(f)

        key = 'return'
        if sig.return_annotation == inspect.Signature.empty:
            f.__annotations__[key] = dict()
        if self._ID not in f.__annotations__[key]:
            f.__annotations__[key][self._ID] = dict()
        f.__annotations__[key][self._ID]["doc"] = self._args[0]

        return f
    # End of __call__()
# End of class _return_decorator

##############################################################################
##############################################################################
### annotizer
##############################################################################
##############################################################################


class annotizer(object):
    """
    This assists in making annotations by providing decorators that are aware
    of your project's internal `UUID <http://en.wikipedia.org/wiki/UUID>`_.
    Using this class will ensure that your annotations are separate from the
    annotations that others use, even if the keys they use are the same as
    your keys.  Thus, projects **A** and **B** can both use the key ''doc''
    while annotating the same function, without accidentally overwriting the
    other project's use.
    """
    def __init__(self, ID,
                 parameter_decorator_class=_parameter_decorator,
                 return_decorator_class=_return_decorator):
        """
        :param ID: This is your project's UUID.  The easiest way to generate
            this is to use the
            `uuid <http://docs.python.org/3/library/uuid.html`_ module, and
            then store the ID somewhere convenient.
        :type ID: ``str`` that can be used to initialize a
            `UUID <http://docs.python.org/3/library/uuid.html#uuid.UUID`_
            instance, or a
            `UUID <http://docs.python.org/3/library/uuid.html#uuid.UUID`_
            instance
        """
        if isinstance(ID, uuid.UUID):
            self._ID = ID
        else:
            self._ID = uuid.UUID(ID)

        self.parameter_decorator_class = parameter_decorator_class
        self.return_decorator_class = return_decorator_class
    # End of __init__()

    def ID():
        doc = ("This is the ID of your project.  It is a " +
               "`UUID <http://docs.python.org/3/library/uuid.html#uuid.UUID`_" +
               "instance.")

        def fget(self):
            return self._ID

        return locals()
    ID = property(**ID())

    def parameter_decorator_class():
        doc = ("Instances of this class may be used to decorate")
        def fget(self):
            return self._parameter_decorator_class
        def fset(self, value):
            self._parameter_decorator_class = value
        def fdel(self):
            self._parameter_decorator_class = _parameter_decorator
        return locals()
    parameter_decorator_class = property(**parameter_decorator_class())

    def return_decorator_class():
        doc = "The return_decorator_class property."
        def fget(self):
            return self._return_decorator_class
        def fset(self, value):
            self._return_decorator_class = value
        def fdel(self):
            self._return_decorator_class = _return_decorator
        return locals()
    return_decorator_class = property(**return_decorator_class())

    def parameter_decorator(self, *args, **kwargs):
        decorator = self.parameter_decorator_class(self.ID, *args, **kwargs)
        return decorator
    # End of parameter_decorator()

    def return_decorator(self, *args, **kwargs):
        decorator = self.return_decorator_class(self.ID, *args, **kwargs)
        return decorator
    # End of return_decorator()
# End of class annotizer

##############################################################################
##############################################################################
### Main
##############################################################################
##############################################################################

if __name__ == "__main__":
    ID1 = uuid.uuid1()
    an1 = annotizer(ID1)
    ID2 = uuid.uuid1()
    an2 = annotizer(ID2)

    @an1.parameter_decorator(a="a", b="b", c="c")
    @an2.parameter_decorator(a="A", b="B", c="C")
    @an1.return_decorator("Doesn't return anything of value")
    @an2.return_decorator("Does not return a value")
    def func(a,b,c):
        print("a = {0!s}, b = {1!s}, c = {2!s}".format(a,b,c))

    pprint.pprint(func.__annotations__)

