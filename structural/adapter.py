""" The Adapter Pattern

Notes:

If the interface of an object does not match the interface required by the
client code, this pattern recommends using an 'adapter' that can create a proxy
interface. It is particularly useful in homogenizing interfaces of 
non-homogenous objects.

The following example represents a use case for adapting various resource 
types to be readable as text resources. We assume that the client programmer
works with resource objects that wrap binary, web-based or textual data. Each
of the aforementioned has its own type and interface but we need to read them
all as text type objects. Since every resource type can be represented as text
(albeit the method calls to do so vary), we use the TextResourceAdapter to
homogenize the interface and output the textual representation using a common
read() method (set to behave like the read() method for TextResource).

"""

class TextResource:
    """We assume that our server can only read text. Therefore this resource is
    the only resource the server knows how to interpret.
    """

    def read(self):
        return "Sample plain text."

class BinaryResource:
    """An instance of this class wraps binary data. While it has many output
    formats, the server can only read the plain-text output.
    """

    def read_plain_text(self):
        return "Sample plain text from binary."

    def read_raw(self):
        pass

    def read_interactive(self):
        pass

class WebResource:
    """An instance of this class wraps web data. While it has many output 
    formats, the server can only read the json output.
    """

    def read_json(self):
        return "Sample plain text as json."

    def read_html(self):
        pass

class IncompatibleResourceError(Exception): 
    pass

class TextResourceAdapter:
    """Acts as an adapter that uses the read() method to return a textual
    representation of the client_resource.
    """

    convertibles = ("TextResource", "BinaryResource", "WebResource")

    def __init__(self, client_resource):
        self._verify_compatibility(client_resource)
        self._client_resource = client_resource

    def read(self):
        """Note that for a resource to use the adapter, it needs to be
        configured beforehand in this method. Your implementation may be
        modified to change this (depending on your use case).
        """

        if self._client_resource.__class__ is BinaryResource:
            return self._client_resource.read_plain_text()

        elif self._client_resource.__class__ is WebResource:
            return self._client_resource.read_json()

        return self._client_resource.read()

    def _verify_compatibility(self, resource):
        """Since we need to pre-configure the adapter to handle various resource
        types, we raise an error if the client_resource is not pre-configured.
        """

        if resource.__class__.__name__ not in self.__class__.convertibles:
            raise IncompatibleResourceError("{} cannot be adapted.".format(
                resource.__class__.__name__))


if __name__ == "__main__":

    client_resources = [BinaryResource(), WebResource(), TextResource()]

    for resource in client_resources:

        print("Adapting {} as a text resource...".format(
            resource.__class__.__name__))

        adapted_resource = TextResourceAdapter(resource)
        # Note how the read interface has been homogenized.
        print(adapted_resource.read() + "\n")