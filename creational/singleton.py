""" The Singleton Pattern

Notes:

While there are multiple ways to implement the Singleton pattern, the point of
the Singleton pattern is to expose only one object without the possiblity to
create multiple _instances of the object.

It is important to note that if your need for this design pattern can be met by
a simple class-less python module (within a .py file), that solution is simpler and
usually preferable. One limitation of using a module's namespace instead of a Singleton
is that a module cannot be constructed with arguments and cannot have properties. 

I strongly recommend the 'Borg' pattern as a more elegant alternative (see borg.py). It
usually meets all the needs of a Singleton with a more classical OOP approach.

"""

class Singleton:
    """The wrapper class serves as an interface for the nested _Singleton class.
    While there may be several instances of this wrapper class, it will always point
    to the same instance of the nested object (Singleton._instance).""" 

    class _Singleton:
        """This nested class should be instantiated only once and assigned to
        Singleton._instance. There should never be a need to interface with it outside
        the scope of the wrapper class."""

        def __init__(self, **kwargs):
            """The exact implementation of the constructor depends on your use case.
            This constructor allows for the setting of an unspecified number of attributes."""

            for key, value in kwargs.iteritems():
                # For a key:value pair of a:1, the next line would equate to `self.a = 1`
                setattr(self, key, value)

    # This will store the one and only instance of _Singleton
    _instance = None

    def __init__(self, **kwargs):
        """The constructor for the wrapper class should only accept arguments for parameters
        that the nested _Singleton can accept. Its purpose is to create an instance of the
        _Singleton if none exists, or to update the instance if it already exists. The exact
        implementation depends on your use case. This implementation allows new instances of
        the wrapper to update previously set attributes of the _instance object and add new
        ones if needed."""

        if not Singleton._instance:
            Singleton._instance = Singleton._Singleton(**kwargs)
        else:
            for key, value in kwargs.iteritems():
                # See line 22 if the line below seems confusing.
                setattr(Singleton._instance, key, value)

    def __getattr__(self, name):
        """This allows the user to access attributes of the _instance via the wrapper."""

        return getattr(self._instance, name)


if __name__ == '__main__':

    """
    Let's suppose our singleton represents the state of all settings for an application.
    While the use case for this example can be met by a dictionary, using a Singleton allows
    you to implement further functionality (such as adding methods).

    For example you could implement a `connect_to_db` method that would try to connect to the
    db at `db_location` if the attribute is set with a valid value.
    """

    app_settings = Singleton(live=True, port=5000)

    # All new instances will point back to the pre-existing Singleton
    # This implementation allows the new constructor to overwrite attributes or add new ones. 
    app_settings_2 = Singleton(port=3000, db_location="far_away")

    # Tests

    print("Do app_settings and app_settings_2 share the same instance?")
    print(app_settings._instance is app_settings_2._instance) # True

    print("Do app_settings and app_settings_2 share the same state?")
    print("live: {}".format(app_settings.live == app_settings_2.live == True)) # True
    print("port: {}".format(app_settings.port == app_settings_2.port == 3000)) # True
    print("db_location: {}".format(app_settings.db_location == app_settings_2.db_location ==
        "far_away")) # True
