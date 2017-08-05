""" The Strategy Pattern

The strategy pattern aims to separate an algorithm's logic from its interface.
This is particularly useful when a client programmer would like to dynamically
select an algorithm from a predefinted set while maintaining the same interface
to use the algorithm. In Python, it is possible to dynamically bind functions to
an object's properties. The following example shows how this makes it really
easy to implement the pattern. 

In this example, the client programmer is provided with a `TreeSearch` strategy
wherein each instance of `TreeSearch` accepts a any kind of `search_runner`
and allows the programmer to run the `search_runner` by calling the `run()`
method. It does so by dynamically binding the specific `search_runner` function
to the `run()` method.
"""

import types

class TreeSearch:
    """Represents a tree search strategy which the client programmer can use."""

    def __init__(self, tree_type, search_runner=None):
        """The constructor accepts a tree_type and a search_runner. The
        search_runner is the function which contains the algorithmic
        implementation of the specific traversal strategy. When provided a
        `search_runner`, it is dynamically binded to `run`, which acts as the
        consistent interface to call the chosen algorithm.
        """

        self.type = tree_type 
        if search_runner:
            self.run = types.MethodType(search_runner, self)

    def run(self):
        """If a `search_runner` is not initialized in the constructor, this
        implementation is used as the default.
        """

        print("Running a Pre-Order DFS search on {}".format(
            self.type))


def run_post_order(self):
    """A function that can be bound to the `run` property of any TreeSearch
    instance dynamically. This would replace the self with a pointer to that
    instance making it behave like an instance method.
    """

    print("Running a Post-Order DFS search on {}".format(
        self.type))

def run_in_order(self):
    """A bindable function (just like `run_post_order`) with a different
    traversal algorithm implemented.
    """

    print("Running a In-Order DFS search on {}".format(
        self.type))


if __name__ == "__main__":

    tree1 = TreeSearch("binary_tree")
    tree1.run()

    tree2 = TreeSearch("red_black_tree", run_post_order)
    tree2.run()

    tree3 = TreeSearch("non_binary_tree", run_in_order)
    tree3.run()