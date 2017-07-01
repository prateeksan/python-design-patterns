""" The Chain of Responsibility Pattern

Notes:

The Chain of Responsibility pattern allows the client programmer to dynamically
create a recursive chain of objects - each of which tries to fulfill a
'responsibility' (usually represented by a method call). If an object in the
chain is unable to fulfill it, the request propagates to the next level of the
chain until it can be fulfilled. This chain is usually implemented as a linked
list (but it can be implemented using other iterable structures).

In the following example, we simulate a service that searches for a job
candidate from several pools of candidates. The pools are categorized by
geographical clusters (local/regional/global) and we assume that the user of
this service wants to find the nearest candidate (in the smallest cluster)
that meets all requirements. The chain of responsibility will thus be a linked
list of the pools which the user will recursively check (smallest to largest)
in order to find a good candidate.
"""

class AbstractPool:
    """The interface for the pool classes. All pools inherit from this."""

    candidates = []

    def __init__(self, successor_pool=None):
        """Note how each pool object can store a pointer to a successor_pool.
        If no such pointer is assigned, we assume that is the last pool in the
        chain.
        """

        self._successor = successor_pool

    def get_match(self, params):
        """If a match is found in the pool of candidates, the candidate is
        returned, else the responsibility is propagated to the next pool in the
        chain.
        """

        match = self._find(params)
        if match:
            return match
        elif self._successor:
                return self._successor.get_match(params)

    def _find(self, params):
        """Returns the first matching candidate in the pool if a match is found.
        The exact implementation of this method is irrelevant to the concept of
        the pattern. It may also be implemented differently for each pool.
        """

        for candidate in self.__class__.candidates:
            if all(key in candidate.items() for key in params.items()):
                print("> Match found in {}:".format(self.__class__.__name__))
                return candidate

        print("> No match found in {}.".format(self.__class__.__name__))

class LocalPool(AbstractPool):

    candidates = [
        {"id": 12, "type": "developer", "level": "intermediate"},
        {"id": 21, "type": "analyst", "level": "junior"}
    ]

class RegionalPool(AbstractPool):

    candidates = [
        {"id": 123, "type": "project_manager", "level": "intermediate"},
        {"id": 321, "type": "designer", "level": "intermediate"}
    ]

class GlobalPool(AbstractPool):

    candidates = [
        # The following candidate is the only one that matches the needs.
        {"id": 1234, "type": "developer", "level": "senior"},
        {"id": 4321, "type": "designer", "level": "senior"}
    ]

if __name__ == "__main__":

    # Setting up recursive propagation in this order: local > regional > global.
    global_pool = GlobalPool()
    regional_pool = RegionalPool(global_pool)
    local_pool = LocalPool(regional_pool)

    print("Searching for a senior developer in the pools chain:")
    print(local_pool.get_match({"type": "developer", "level": "senior"}))