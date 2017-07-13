""" The Mediator Pattern

Notes:

In situations where there is a need to create and manage many to many
relationships between objects, the mediator pattern provides an elegant solution
by creating an intermediary object that maintains these relationships. All
related objects maintain a pointer to the mediator and the mediator maintains
pointers to all the aforementioned. This allows communication between objects
that have no knowledge of each other (thus coupling them loosely).

The following example uses the pattern to manage a network of nodes with complex
internal relationships.
"""

class Mediator:
    def __init__(self):
        self._nodes = []

    def register_member(self, member):
        self._nodes.append(member)

    def toggle(self, source, activate):
        if source.type == 'master':
            self._toggle_all(activate)
        elif source.type == 'local_master':
            self._toggle_local(local_group=source.local_group, 
                activate=activate)
        else:
            print("{} {} node.".format(
                'Activating' if activate else 'Deactivating', source.name))
            source.active = activate

    def _toggle_all(self, activate):
        print("{} all nodes".format(
            'Activating' if activate else 'Deactivating'))
        for node in self._nodes:
            node.active = activate

    def _toggle_local(self, local_group, activate):
        print("{} all nodes in the {} local group.".format(
            'Activating' if activate else 'Deactivating', local_group))
        for node in self._nodes:
            if node.local_group == local_group and node.type != 'master':
                node.active = activate

    def print_network_status(self):

        print("Following is the state of all nodes in the network:")
        for node in self._nodes:
            print("\t > " + str(node))

class Node:

    def __init__(self, mediator, name, n_type, local_group):
        self.mediator = mediator
        self.name = name
        self.type = n_type
        self.local_group = local_group
        self.mediator.register_member(self)
        self.active = False

    def activate(self):
        self.mediator.toggle(source=self, activate=True)

    def deactivate(self):
        self.mediator.toggle(source=self, activate=False)

    def __repr__(self):
        return ("Name: {}, Active: {}".format(
            self.name, self.active))


if __name__ == '__main__':

    mediator = Mediator()
    master_node = Node(mediator, 'root', 'master', 'global')
    # Local group 1 (G1)
    g1_master = Node(mediator, 'g1_root', 'local_master', 'G1')
    g1_node_a = Node(mediator, 'g1_a', 'general', 'G1')
    g1_node_b = Node(mediator, 'g1_b', 'general', 'G1')
    # Local group 2 (G2)
    g2_master = Node(mediator, 'g2_root', 'local_master', 'G2')
    g2_node_a = Node(mediator, 'g2_a', 'general', 'G2')
    g2_node_b = Node(mediator, 'g2_b', 'general', 'G2')

    master_node.activate()
    g1_master.deactivate()
    g1_node_b.activate()

    mediator.print_network_status()
