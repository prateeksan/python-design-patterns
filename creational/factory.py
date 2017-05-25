""" The Factory Pattern

Notes:


"""

from __future__ import generators
import random

class Parent(object):

    def __init__(self, lifespan):

        self.lifespan = lifespan

    @staticmethod
    def factory(object_class, lifespan):

        for Child in Parent.__subclasses__():
            if Child.__name__ == object_class:
                return Child(lifespan)

        return False

class HappyChild(Parent):
    pass

class UnhappyChild(Parent):
    pass

def child_generator(count, parent, life_min, life_max):
    types = parent.__subclasses__()
    for i in range(count):
        yield {"class": random.choice(types).__name__, 
            "lifespan": random.randint(life_min, life_max)}

if __name__ == '__main__':

    print("Generating 5 children of 'Parent' with a random lifespan between 0 - 99:")

    children = [ Parent.factory(params["class"], params["lifespan"])  \
        for params in child_generator(count=4, parent=Parent, life_min=0, life_max=99)]

    for child in children:
        print(type(child).__name__, child.lifespan)