""" The Memento Pattern

Notes:


"""

import copy

class MapCheckpoint:

    def __init__(self, map_state, message):

        self.map_state = map_state
        self.message = message

class MapBuilder:

    def __init__(self, map_size):
        self.map_size = map_size
        self.map = self._build_default_map()

    def draw(self, coords, value):

        if not (coords[0] < self.map_size[0] and coords[1] < self.map_size[1]):
            print("Coordinates not in range. Try again!")
            return False

        print("Drawing '{}' to coords: ({},{}).".format(value, coords[0], 
            coords[1]))
        self.map[coords[1]][coords[0]] = value

    def create_checkpoint(self, message):

        print("Creating new checkpoint: <{}>".format(message))
        return MapCheckpoint(map_state=copy.deepcopy(self.map), message=message)

    def restore_from_checkpoint(self, checkpoint):
        print("Restoring to checkpoint: <{}>".format(checkpoint.message))
        self.map = copy.deepcopy(checkpoint.map_state)

    def _build_default_map(self):
        return [["-" for x in range(self.map_size[0])] 
            for y in range(self.map_size[1])]

    def print_map(self):
        for row in self.map:
            print(row)
        print("\n")

class CheckpointLog():

    def __init__(self, max_length=3):
        self._checkpoints = []
        self.max_length = max_length

    def add(self, new_checkpoint):

        if len(self._checkpoints) == self.max_length:
            del self._checkpoints[0]

        self._checkpoints.append(new_checkpoint)

    def revert(self, revert_count=1):
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
    map_builder.print_map()
