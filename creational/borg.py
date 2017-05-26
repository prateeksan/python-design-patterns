""" The Borg Pattern

Notes:

Originally proposed by Alex Martelli, the Borg Pattern improves upon the classical
Singleton pattern by questioning the point of a Singleton. While a Singleton
design pattern mandates that all objects representing a Singleton must share 
the same identity (point to the same instance of a class), the Borg pattern
allows all representations to have unique identities (instances) while ensuring that 
they all share the same state (all attributes of the instances point to the same 
dictionary).

Many Python developers consider the Singleton to be an anti-pattern (If all 
representations are to point to the same instance, why not just use a class-less 
module with functions and variables?). The Borg pattern solves this problem by 
allowing for a shared state while simultaenously allowing for meaningful inheritance
and preservation of object identities.

"""

class Borg:
    """Any children of this Borg class will share its state but
    NOT its identity."""

    _shared_state = {}

    def __init__(self):
        """All attributes of an instance of a Python class are added by 
        default to the `self.__dict__` dictionary. The Borg pattern exploits this
        by binding the `__dict__` attribute for all child instances to the 
        `_shared_state` dictionary."""

        self.__dict__ = self._shared_state

class ChildBorg(Borg):

    def __init__(self, **kwargs):
        """In this example, by calling the Borg's constructor, 
        `self.__dict__` is binded before its attributes are assigned.
        This will ensure the instance has access to all of the `_shared_state`
        attributes, and that its attribute assigments will update the shared state."""

        # Construct the Borg before setting attributes to bind the shared state.
        Borg.__init__(self)
        # How attributes are assigned henceforth depends entirely on your needs.
        # This example allows the constructor to accept and assign multiple unknown attributes.
        for key, value in kwargs.iteritems():
            # For a key:value pair of a:1, the next line would equate to `self.a = 1`
            setattr(self, key, value)


if __name__ == '__main__':

    # Let's imagine our Borg represents a type of video game character.
    cb1 = ChildBorg(health=100, attack=15)

    # Let's suppose that some in-game event causes all Borgs to become 10% healthier
    # and gain an armour worth 20 points.

    # Creating a new ChildBorg after the aformenetioned ingame event.
    cb2 = ChildBorg(health=110, attack=15, armour=20)

    # Tests

    print("Do cb1 and cb2 have separate identities?")
    print(cb1 is not cb2) # True

    print("Do cb1 and cb2 share the same state?")
    print("Health: {}".format(cb1.health == cb2.health == 110)) # True
    print("Attack: {}".format(cb1.attack == cb2.attack == 15)) # True
    print("Armour: {}".format(cb1.armour == cb2.armour == 20)) # True (note how cb1 also has armour)
