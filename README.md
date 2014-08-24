=====================
The annotizer project
=====================

The annotizer project has two goals.  The project's main goal is to introduce
a convention for annotizing functions and methods that allows multiple
projects to share an annotation dictionary without conflicts.  Thus, a linter
and a documentation project can both be used on the same project at the same
time.  The following example may make things clearer::

    # Actual convention uses UUID instances, these strings are for example
    # only.

    an1 = annotizer("The linter's unique ID")
    an2 = annotizer("The documentor's unique ID")

    @an1.type_decorator(a=str, b=str, c=str)
    @an2.parameter_decorator(a="A", b="B", c="C")
    @an1.rtype_decorator(None)
    @an2.return_decorator("Does not return a value")
    def func(a, b, c):
        print("a = {0!s}, b = {1!s}, c = {2!s}".format(a,b,c))

In the example, both sets of annotations coexist without harming one another
because the annotations themselves are stored in a dictionary that is keyed by
the unique IDs of each project.

The example actually shows the secondary goal of the project; to define a
series of decorators that can be used that are compliant with the convention.

=======================
The Proposed Convention
=======================

I propose that all annotations be dictionaries keyed by some unique
identifier.  The annotation dictionary for ``func`` from the prior section
would be::

    # Actual convention uses UUID instances, these strings are for example
    # only.

    {'a': {"The linter's unique ID": {'type': str},
           "The documentor's unique ID": {'doc': 'A'}},
     'b': {"The linter's unique ID": {'type': str},
           "The documentor's unique ID": {'doc': 'B'}},
     'c': {"The linter's unique ID": {'type': str},
           "The documentor's unique ID": {'doc': 'C'}},
     'return': {"The linter's unique ID": {'type': None},
                "The documentor's unique ID": {'doc': 'Does not return a value'}}}

In this case, neither the documentation project, nor the linter project had
any knowledge of the other.  Both were used successfully in a third project,
without harming the other.  I believe that this is the correct way forward to
ensure that we can all use the annotation dictionary without conflict.

===================
Why UUID Instances?
===================

Humans are **terrible** at choosing unique names, and programmers are trained
to be even worse.  As programmers, we want to make our code as clear as
possible; that means that different programmers that are working to solve the
same problem are likely to use the same name for their projects.  To prevent
this from becoming a serious problem, I propose that we use ``uuid.UUID``
instances exclusively.  The code currently rejects anything that isn't a
`uuid.UUID <https://docs.python.org/3/library/uuid.html#uuid.UUID>`_ instance.

==============
Current Status
==============

The code is currently only a proof-of-concept.  The easiest way to see how it
works is to read it.  I know that there are shortcomings; suggestions or
patches are welcome!
