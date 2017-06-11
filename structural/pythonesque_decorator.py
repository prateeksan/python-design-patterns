""" The Pythonesque Decorator Pattern(!?)

Disclaimer: Python Decorators and the decorator pattern are not the same. Python
decorators are an idiosyncratic feature of the language while the decorator
pattern can be implemented in any language. Having said that, I failed to find a
use case for the normal implementation of the decorator pattern in Python (given
the presence of the decorator feature). Therefore, I have to decided to combine
the two and produce this unusual but useful variation of the pattern. All
skepticism and criticism is welcome.

Notes: The decorator pattern's key objective is to allow for a more flexibile
alternative to inheritance to add behaviour and attributes to an object.
As per the traditional implementation, you would wrap the object recursively in
children of its own type (which in turn would wrap method calls and add more
behaviour before or after the function call). I found this traditional pattern
to be really counter-intuitive; here's why:

+ It does not really avoid inheritance. It just uses it to maintain a consistent
interface. This makes it really complicated to manage internal state, identity
etc.

+ You have to force the decorator class to implement all of the methods of the,
wrapped class (in order to call the method in the wrapped object). I don't see
why it wouldn't make more sense to just dynamically change the type of the 
object and use inheritance instead (yes Python can do this).

In the following implementation, I attempt to overcome these limitations using
the decorator feature in an unusual way. The `validate_inputs` decorator wraps
an entire class and only decorates specific methods (in this case anything that
starts with 'input_'). Furthermore, it accepts a list of functions which are set
as decorators of the methods in question. It also maintains the order of the
decorators as they are set to the methods. It can be used as a more flexible
alternative to multiple inheritance without the aforementioned drawbacks.

"""

def validate_inputs(decorators):
    """This function decorates a class and dynamically sets a list of
    decorators to methods of the object that begin with 'input_'."""

    def decorate(cls):
        for method in dir(cls):
            # More complex conditions for method filtering may be used here.
            if callable(getattr(cls, method)) and \
                method.startswith("input_"):
                # Reversal ensures that decorators are added in the given order.
                for decorator in reversed(decorators):
                    setattr(cls, method, decorator(getattr(cls, method)))
        return cls
    return decorate

def is_string(func):
    """This decorator prevents the method from executing normally if the input
    is not a string."""

    def wrapper(self, text):
        if type(text) is not str:
            return "'{}' is invalid. Input should be a string.".format(text)
        return func(self, text)
    return wrapper

def is_lowercase(func):
    """This method decorator prevents the method from executing normally if the
    the input is not lowercase."""

    def wrapper(self, text):
        if not text.islower():
            return "'{}' is invalid. Input should be lowercase.".format(text)
        return func(self, text)  
    return wrapper

# Note how is_lowercase is set after is_string.
@validate_inputs([is_string, is_lowercase])
class TextForm():
    """Any input passed into objects of this type will go through two
    validations as set in the `validate_inputs` decorator. Note that inheritance
    is not used at all in the assignment of such additional behaviour. The
    `validate_inputs` decorator (and all the decorators passed to it) can be set
    on any type of object."""

    def input_username(self, name): 
        return  "'{}' is valid. Input registered.".format(name)

    def input_team_name(self, team):
        return "'{}' is valid. Input registered.".format(team)

    def special_input_comments(self, comments):
        return "Comments are always valid!"

if __name__ == "__main__":

    form = TextForm()

    print("Attempting to input username:")
    print(form.input_username("PrateekSan"))
    print(form.input_username(123))
    print(form.input_username("prateeksan"))
    print(form.input_team_name(2.1))

    print("\n" + "Attempting to input team name:")
    print(form.input_team_name("TeamPratt"))
    print(form.input_team_name("team_pratt"))

    print("\n" + "Attempting to input comments:")
    print(form.special_input_comments("THIS IS ALL UPPERCASE"))

    print("\n")