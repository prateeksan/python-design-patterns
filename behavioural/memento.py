""" The Memento Pattern

Notes:

The Memento pattern allows an object to maintain a history of its state external
to itself (thus allowing it to perform reverts). The need to maintain version 
history or revert to an older state can be handled in several ways. The Command
and Memento pattern offer two competing ways, each with its own pros and cons.
The Command pattern allows the invoker to revert the Commands which caused
the change of state while maintaining no knowledge of the state of the different
versions. The Memento on the other hand does not log the actions that changed
state; rather it caches a copy of the changed state at chosen iterations. 

This makes the Command pattern more space efficient but potentially slower (each 
actions must be un-performed in reverse order until a desired state is reached).
It also introduces the problem of trying to revert Commands with a non-trivial
action to undo its changes. The Memento pattern resolves the aforementioned
problem and significantly improves time complexity of reverts (any recorded
state can be reverted to in constant time), but it significantly worsens space
complexity by storing a full copy of the changed state at every checkpoint.

The following example simulates a virtual map builder which allows a user to
build a tile based map, while being able to save checkpoints of their progress
and return to an older state at any time. The Memento pattern depends on three
objects - an 'Originator', implemented in this example as a 'MapBuilder' which
stores the internal state that needs version controlling; a 'Caretaker',
implemented as the 'CheckpointLog' which stores a historical log of different 
versions of the originators state; and a 'Memento', in this case the
'MapCheckpoint' which stores a saved version of the state (the map) along with
other relevant meta data (a checkpoint message).
"""

import copy

class MapCheckpoint:
    """Acts as the Memento and stores a snapshot state of the map along with
    a message describing the checkpoint.
    """

    def __init__(self, map_state, message):

        self.map_state = map_state
        self.message = message

class MapBuilder:
    """Acts as the Originator and is responsible for creating, drawing and
    maintaining the map. It is also responsible for creating checkpoints at
    relevant intervals which are stored in an external log. The state of the
    map can then be reverted to the stored checkpoints at any point.
    """

    def __init__(self, map_size):
        """The map can be constructed with a variable size."""

        self.map_size = map_size
        self.map = self._build_default_map()

    def draw(self, coords, value):
        """Called by the user to add a new value to a tile."""

        if not (coords[0] < self.map_size[0] and coords[1] < self.map_size[1]):
            print("Coordinates not in range. Try again!")
            return False

        print("Drawing '{}' to coords: ({},{}).".format(value, coords[0], 
            coords[1]))
        self.map[coords[1]][coords[0]] = value

    def create_checkpoint(self, message):
        """Creates and returns a snapshot memento of the map's state as a 
        MapCheckpoint object.
        """

        print("Creating new checkpoint: <{}>".format(message))
        return MapCheckpoint(map_state=copy.deepcopy(self.map), message=message)

    def restore_from_checkpoint(self, checkpoint):
        """Restores the state of a map from a MapCheckpoint. Note how the
        MapBuilder has no knowledge of logged checkpoints.
        """

        print("Restoring to checkpoint: <{}>".format(checkpoint.message))
        self.map = copy.deepcopy(checkpoint.map_state)

    def _build_default_map(self):
        """Builds a 2d map of the given size with '-' default values."""

        return [["-" for x in range(self.map_size[0])] 
            for y in range(self.map_size[1])]

    def print_map(self):

        for row in self.map:
            print(row)
        print("\n")

class CheckpointLog():
    """Acts as the caretaker and is responsible for maintaining a history of the
    checkpoints (mementos) created. It can also load and return a previous
    checkpoint. One instance of this class should be used to record checkpoints
    for one instance of the MapBuilder.
    """

    def __init__(self, max_length=3):
        """The user may specify a max_length for the log which defaults to 3.
        This represents the max checkpoints that can be recorded for one map
        builder.
        """

        self._checkpoints = []
        self.max_length = max_length

    def add(self, new_checkpoint):
        """Adds a new MapCheckpoint instance and deletes the oldest one."""

        if len(self._checkpoints) == self.max_length:
            del self._checkpoints[0]

        self._checkpoints.append(new_checkpoint)

    def revert(self, revert_count=1):
        """Returns an older MapCheckpoint. In a real use-case, this method may
        also be responsible for re-arranging or deleting checkpoints posterior
        to the reverted.
        """

        return self._checkpoints[-revert_count]


if __name__ == "__main__":

    map_builder = MapBuilder((3,3))
    cp_log = CheckpointLog()

    map_builder.draw(coords=(2,2), value="x")
    cp_log.add(map_builder.create_checkpoint("Only one 'x'"))
    map_builder.print_map()

    map_builder.draw(coords=(2,1), value="y")
    cp_log.add(map_builder.create_checkpoint("One 'x' and one 'y'"))
    map_builder.print_map()

    map_builder.draw(coords=(2,2), value="y")
    cp_log.add(map_builder.create_checkpoint("Two 'y's"))
    map_builder.print_map()

    map_builder.restore_from_checkpoint(cp_log.revert(3))
    map_builder.print_map() # The ouput should be the same as line 137
