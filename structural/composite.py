""" The Composite Pattern

Notes:

If you have used trees before, you would know that they are extremely useful in
representing hierarchical data. The composite pattern extends this truism to
the OOP realm by organizing objects with a hierarchical relationship in a tree.
One important point to note is that in the composite pattern, composite objects
(trees) and primitive objects (leaf nodes) need to offer uniformity in their
interface to a reasonable extent. The user should be able to perform some
operations on a node without knowing the type of node (composite or leaf).
Other operations may indeed need a knowledge of the node type. How much of the
interface should be uniform depends on your use case.

The example below illustrates a use case for storing simple, readable data. The
DataObject defines the common interface between composite nodes and leaf nodes.
The DataNode represents a leaf node and contains non-composite data. The
DataComposite represents trees with an interface to add and remove child nodes.

"""

class DataObject():
    """Both composite and leaf data types inherit from this. It defines the
    common interface for both data object types. While this implementation does
    not require a pointer to the parent node, this may be added as per your use
    case.
    """

    def read(self): pass

class DataNode(DataObject):
    """Represents a primitive (non-composite) data object which can be used as a
    leaf node in the tree."""

    def __init__(self, data):
        self._data = data

    def read(self):
        print("Node Data: {}".format(self._data))

class DataComposite(DataObject):
    """Represents a composite data object (tree). Its instances can act as
    independent trees or sub-trees for other composite objects)."""

    def __init__(self, data):
        """Note how the data argument is handled differently for DataComposite
        objects and DataNode objects. The data passed to a composite object is
        set as meta data about the composite set. The user need not know this
        while passing the data."""

        self._meta_data = data
        self.sub_objects = []

    def read(self):
        """Note how the user can call the read method on all children of
        DataObject and get a desired response even though the method's behaviour 
        differs in the child classes."""

        print("Data Composite For: {}".format(self._meta_data))
        for data_object in self.sub_objects:
            data_object.read()

    def add(self, data_object):
        self.sub_objects.append(data_object)

    def remove(self, data_object):
        self.sub_objects.remove(data_object)


if __name__ == "__main__":

    # Creating primitive (leaf) data nodes.
    python = DataNode("Python")
    ruby = DataNode("Ruby")
    english = DataNode("English")
    french = DataNode("French")

    # Creating composite data nodes.
    lang_tree = DataComposite("Languages")
    programming_lang_tree = DataComposite("Programming Languages")
    human_lang_tree = DataComposite("Human Languages")

    # Adding primitive nodes as sub objects (children).
    programming_lang_tree.add(python)
    programming_lang_tree.add(ruby)
    human_lang_tree.add(english)
    human_lang_tree.add(french)

    # Adding composite nodes as sub objects (children).
    lang_tree.add(human_lang_tree)
    lang_tree.add(programming_lang_tree)

    # The read method call is type agnostic even though its behaviour differs.
    lang_tree.read()


