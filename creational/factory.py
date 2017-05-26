""" The Factory (Method) Pattern

Notes:

The Factory Pattern serves to introduce a layer of abstraction in the
object creation process. The factory serves as a common interface to construct
objects of multiple types. This can be particularly useful to manage object creation
in an organized and easily testable manner. Furthermore, the object creation factory
may be able to identify which type of object to construct based on some information
about the required nature of the object. For example, a factory that generates
objects with a base class 'Car' may be instructed to generate a car with `top_speed > n`
and `fuel_type == 'biodiesel'`; this factory might then generate a type (child) of `Car`
that matches these specifications.

There are many ways to implement this design pattern. The example shown below, known as
the 'Factory Method Pattern', is a very straightforward implementation. It is useful when
the factory is resoponsible for returning objects of multiple types that all share a
common parent. In this pattern, the factory is implemented as a static method of the
parent class, and can return objects of child classes based on some information about
the expected object type (passed as arguments to the factory method). If your factory
is expected to return objects with no known common parent class, the factory can easily
be implemented as a standalone function or within an independent `Factory` class.

"""

from __future__ import generators
import random

class Parent(object):
    """This class serves as the base class for all object types that the factory
    can produce."""

    def __init__(self, lifespan):
        """In this example, we will set a lifespan attribute to the parent (inherited by
        all its children). It is for demonstrative purposes only and is not pertinent
        to the Factory Pattern."""

        self.lifespan = lifespan

    @staticmethod
    def make_child(name, args):
        """This is the factory method. It creates a layer of abstraction wherein
        it can create and return objects based on some information about the object. In
        this case we are simply supplying the name of the object type as string but you
        could easily include more complex logic to derive the required object type based
        on less direct information."""

        for Child in Parent.__subclasses__():
            if Child.__name__ == name:
                return Child(*args)

        return False

class TypeAChild(Parent):
    pass

class TypeBChild(Parent):
    pass

def generate_children(count, parent, life_min, life_max):
    """We are using a generator to randomly seed a sequence of specifications for the
    factory. While this is not strictly part of the Factory Pattern, it can be useful
    for testing the factory or for generating objects based on some pre-defined algorithm.
    It is perfectly acceptable to implement factories without generators (depends on your
    specific use-case)."""

    types = parent.__subclasses__()
    for i in range(count):
        yield { 
            "class_name": random.choice(types).__name__, 
            "lifespan": random.randint(life_min, life_max)
        }

if __name__ == '__main__':

    print("Generating 10 children of 'Parent' with a random lifespan between 0 - 99:")

    # The generator and factory work in cohesion to algorithmically generate objects.
    children = [Parent.make_child(name=params["class_name"], args=[params["lifespan"]]) \
        for params in generate_children(count=10, parent=Parent, life_min=0, life_max=99)]

    for child in children:
        print(type(child).__name__, child.lifespan)