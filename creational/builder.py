""" The Builder Pattern

Notes:

"""

# A generalized director that can handle various abstract builders
class GeneralDirector():

    def __init__(self, AbstractBuilder):
        self.AbstractBuilder = AbstractBuilder
        self.build_methods = self.get_build_methods()
        self.concrete_builder = None

    def get_build_methods(self):

        method_list = []

        for method in dir(self.AbstractBuilder):
            if callable(getattr(self.AbstractBuilder, method)) and \
                method.startswith("build_"):
                method_list.append(method)

        return method_list

    def build(self):

        self.concrete_builder.new_meal()

        for method_name in self.build_methods:
            method = getattr(self.concrete_builder, method_name)
            method()

    def get_product(self):
        return self.concrete_builder.meal

# Abstract builder for all meals.
class AbstractMealBuilder():

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
