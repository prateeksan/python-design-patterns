""" The Registry Pattern

Notes:

The registry pattern is both very simple and very handy. It allows you to
maintain a record (registry) of all subclasses of a certain class. This can be
useful for managing, interacting with or dynamically updating the behaviour of
all subclasses in a code base. Since all Python classes are instances of the 
'type' metaclass, a very intuitive way to implement this pattern is to create
a subclass of 'type' and use it as the metaclass for the base class whose
children will be registered.

In this example, the 'ErrorMeta' acts as a meta class for 'BaseError' and all
its children. We assume that all errors (Exceptions) in this hypothetical
codebase will be subclasses of 'BaseError'. We also assume that all such errors
will have a meaningful 'code' which is set as the class attribute. The 
'registry' attribute of the metaclass thus maintains a dictionary of all
subclasses of 'BaseError' with the error code of the subclass as the key.

"""

class ErrorMeta(type):
    """Acts as the meta class for BaseError and its subclasses. In this example,
    the registry is implemented as a simple dictionary but this may be modified
    depending on the use case. For example, it may be useful to implement the
    registry as a tree or graph that maps the inheritance chain of the 
    registered classes.
    """

    registry = {}

    def __new__(cls, *args, **kwargs):
        new_error_type = type.__new__(cls, *args, **kwargs)
        # In this example, the error code acts as the key to identify the type.
        cls.registry[new_error_type.code] = new_error_type
        return new_error_type

class BaseError(Exception):
    """By default, the __metaclass__ is always 'type'. By overriding this to be
    ErrorMeta, we ensure that this class and all its subclasses will invoke
    ErrorMeta.__new__ and consequently be added to the registry.
    """

    __metaclass__ = ErrorMeta
    code = 999

if __name__ == "__main__":

    print("Registry with only the BaseError implemented:")
    print(ErrorMeta.registry)

    class ClientError(BaseError):
        code = 400

    class ServerError(BaseError):
        code = 500

    print("\nRegistry with client and server errors implemented:")
    print(ErrorMeta.registry)
