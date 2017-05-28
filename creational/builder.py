""" The Builder Pattern

Notes:

The Builder Pattern is particularly useful for creating complex objects made up of
several smaller objects. This pattern uses classes to represent both objects and their
builders (used to assemble objects). By having all child builders inherit from an
abstract builder, it is possible to place restrictions on the implementations of all
child builders by changing code in just the abstract builder class. Furthermore, allowing
only director objects to use the builders ensures control over object creation (similar
to the Factory Pattern).

In this example, the director class (GeneralDirector) has been implemented in a manner
wherein it can be insantiated to handle any abstract builder (as long as all its build
methods start with 'build_'). The following implementation simulates a virtual takeout
restaurant that needs to assemble complex meals. While the Meal object in this case is
not very complex, it is easy to see how the implementation could scale to match complexity
in this design (for example, the build methods might need to change the state of SQL
table(s) containing an inventory of resources required to build its object). 

"""

class GeneralDirector():
    """A generalized director that can handle various abstract builders. It is also common
    practice to implement directors specifically designed to handle only certain types of
    builders. The key is to ensure that it acts as the sole interface to the builders.
    """

    def __init__(self, AbstractBuilder):
        """Constructs an instance while setting an AbstractBuilder and identifying all its
        build methods.
        """

        self.AbstractBuilder = AbstractBuilder
        self.build_methods = self.get_build_methods()
        self.concrete_builder = None

    def get_build_methods(self):
        """This method should be called when the AbstractBuilder is assigned. The director
        will run only the build methods returned by this method."""

        method_list = []

        for method in dir(self.AbstractBuilder):
            if callable(getattr(self.AbstractBuilder, method)) and \
                method.startswith("build_"):
                method_list.append(method)

        return method_list

    def build(self):
        """Calling this method creates a new product by calling all build functions.
        It provides a layer of abstraction which allows the caller to build the complex
        object without having to manually construct it each time."""

        self.concrete_builder.new_meal()

        for method_name in self.build_methods:
            method = getattr(self.concrete_builder, method_name)
            method()

    def get_product(self):
        """Returns the final object or its placeholder."""

        return self.concrete_builder.meal

class AbstractMealBuilder():
    """An abstract builder serves as the parent class for a set of concrete builders.
    No object should be built by directly instantiating the abstract builder. Note
    how all build functions are set to raise a `NotImplementedError`. This forces
    the child builder to ensure that all requisite parts of the final object are built
    since the GeneralDirector object will always call all build methods.
    """

    def __init__(self):
        self.meal = None

    def new_meal(self):
        self.meal = Meal(self.__class__.meal_name)

    def build_food(self):
        raise NotImplementedError

    def build_cutlery(self):
        raise NotImplementedError

    def build_package(self):
        raise NotImplementedError

    def build_bill(self):
        raise NotImplementedError

class TakeoutSpecialBuilder(AbstractMealBuilder):
    """This concrete builder serves to build a certain kind of meal. Usually,
    most of the complex creational logic would be implemented in the build functions
    here. In this example, all build functions bound to the abstract builder
    must be implemented here (while new ones may be implemented, doing so may create
    confusion in a large code base)."""

    meal_name = "Takeout Special"
    
    def build_food(self):
        self.meal.food = ["Egg Noodles", "Fortune Cookie"]

    def build_cutlery(self):
        self.meal.cutlery = ["Chopsticks", "Fork"]

    def build_package(self):
        self.meal.package = "Takeout Box"

    def build_bill(self):
        self.meal.bill = 10.50

class CheeseBurgerBuilder(AbstractMealBuilder):
    """Please see docstring for the `TakeoutSpecialBuilder`. This class serves
    the same purpose to build a different kind of meal."""

    meal_name = "Cheese Burger"
    
    def build_food(self):
        self.meal.food = ["Cheese", "Patty", "Buns"]

    def build_cutlery(self):
        self.meal.cutlery = ["Butter Knife"]

    def build_package(self):
        self.meal.package = "Paper Bag"

    def build_bill(self):
        self.meal.bill = 8.00 

# Product
class Meal():
    """This class will be instantiated to represent the object that is being built.
    It can be implemented in any manner as long as its construction can be handled
    by the concrete builders. In this example, multiple concrete builders build this
    type of object (with different attribute values)."""

    def __init__(self, name):

        self.name = name
        self.food = None
        self.cutlery = None
        self.package = None
        self.bill = None

    def __repr__(self):
        return "<Meal: {}>".format(self.name)

    def pretty_print(self):

        print("Order Type : {}".format(product.name))
        print("Food       : {}".format(
            (", ").join(product.food)
        ))
        print("Cutlery    : {}".format(
            (", ").join(product.cutlery)
        ))
        print("Package    : {}".format(self.package))
        print("Bill       : {}".format(self.bill))
        print("\n")

# Interface
if __name__ == "__main__":

    director = GeneralDirector(AbstractBuilder=AbstractMealBuilder)
    
    # Build Takeout
    director.concrete_builder = TakeoutSpecialBuilder()
    director.build()
    product = director.get_product()
    product.pretty_print()

    # Build CheeseBurger
    director.concrete_builder = CheeseBurgerBuilder()
    director.build()
    product = director.get_product()
    product.pretty_print()
