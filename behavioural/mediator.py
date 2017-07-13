""" The Mediator Pattern

Notes:

In situations where there is a need to create and manage many to many
relationships between objects, the mediator pattern provides an elegant solution
by creating an intermediary object that maintains these relationships. All
related objects maintain a pointer to the mediator and the mediator maintains
pointers to all the aforementioned. This allows communication between objects
that have no knowledge of each other (thus coupling them loosely).

The following example uses the pattern to manage a network of nodes with complex
internal relationships. In this network, there are three types of nodes - master
node(s), local_master node(s) and general node(s). Each node has an activate and
deactivate switch (method) which toggles its 'active' state (attribute).
Toggling a master node activates or deactivates the entire network. Toggling a 
local_master node does the same for all nodes in its local group (except global
master nodes). Toggling a general node only affect its own state. Lastly, every
node belongs to only one local group. 
"""

class NetworkMediator:
    """Responsible for maintaining relationships between all nodes. It does so
    by managing the 'active' state of all nodes, conforming to the behavioural
    rules defined in the aforementioned docstring.
    """

    def __init__(self):
        self._nodes = []

    def register_member(self, member):
        """When a node is added to the network, the mediator is made aware of it
        by the node itself (who calls this method). In other words, both the
        node and the mediator are aware of each other.
        """

        self._nodes.append(member)

    def toggle(self, source, activate):
        """When someone activates or deactivates a node, this method is called
        by the node. Rather than the node having to manage its own state and the
        state of other affected nodes in the network, the mediator takes care
        of it all. Note how this creates a loose coupling between the nodes.
        This is the meat of the mediator pattern.
        """

        if source.type == 'master':
            self._toggle_all(activate)
        elif source.type == 'local_master':
            self._toggle_local(local_group=source.local_group, 
                activate=activate)
        else:
            print("{} the {} node.".format(
                'Activating' if activate else 'Deactivating', source.name))
            source.active = activate

    def _toggle_all(self, activate):
        """Toggles the state of all nodes (triggered by toggling a master)."""

        print("{} all nodes".format(
            'Activating' if activate else 'Deactivating'))
        for node in self._nodes:
            node.active = activate

    def _toggle_local(self, local_group, activate):
        """Toggles the state of all nodes in a local group (triggered by
        toggling a local master).
        """

        print("{} all nodes in the {} local group.".format(
            'Activating' if activate else 'Deactivating', local_group))
        for node in self._nodes:
            if node.local_group == local_group and node.type != 'master':
                node.active = activate

    def print_network_status(self):
        """Prints the status of all nodes managed by the mediator."""

        print("Following is the state of all nodes in the network:")
        for node in self._nodes:
            print("\t > " + str(node))

class Node:
    """Represents a node in the network. The only thing it interacts with in its
    network is the network mediator.
    """

    def __init__(self, mediator, name, n_type, local_group):
        """Construct a node with all its attributes and a pointer to its
        mediator.
        """

        self.mediator = mediator
        self.name = name
        self.type = n_type
        self.local_group = local_group
        self.mediator.register_member(self)
        self.active = False

    def activate(self):
        """Informs the mediator to activate this node and all nodes affected by
        it. The node maintains no knowledge of which other nodes will be
        activated.
        """

        self.mediator.toggle(source=self, activate=True)

    def deactivate(self):
        """Informs the mediator to deactivate this node and all nodes affected 
        by it. The node maintains no knowledge of which other nodes will be
        deactivated.
        """

        self.mediator.toggle(source=self, activate=False)

    def __repr__(self):
        return ("Name: {}, Active: {}".format(
            self.name, self.active))


if __name__ == '__main__':

    mediator = NetworkMediator()
    master_node = Node(mediator, 'root', 'master', 'global')
    # Local group 1 (G1)
    g1_master = Node(mediator, 'g1_root', 'local_master', 'G1')
    g1_node_a = Node(mediator, 'g1_a', 'general', 'G1')
    g1_node_b = Node(mediator, 'g1_b', 'general', 'G1')
    # Local group 2 (G2)
    g2_master = Node(mediator, 'g2_root', 'local_master', 'G2')
    g2_node_a = Node(mediator, 'g2_a', 'general', 'G2')
    g2_node_b = Node(mediator, 'g2_b', 'general', 'G2')

    master_node.activate() # Activates all nodes.
    g1_master.deactivate() # Deactivates all nodes in the G1 group.
    g1_node_b.activate() # Activates only itself.

    print("\n")
    mediator.print_network_status()
