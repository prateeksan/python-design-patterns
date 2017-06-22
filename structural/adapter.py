""" The Adapter Pattern

Notes:

If the interface of an object does not match the interface required by the
client code, this pattern recommends using an 'adapter' that can create a proxy
interface. It is particularly useful in homogenizing interfaces of 
non-homogenous objects. 

"""

class TextResource():
    """
    """

    def read(self):
        return "Sample plain text."

class BinaryResource():
    def read_plain_text(self):
        return "Sample plain text from binary."

    def read_raw(self):
        pass

    def read_interactive(self):
        pass

class WebResource():
    def read_json(self):
        return "Sample plain text from json."

    def read_html(self):
        pass

class IncompatibleResourceError(Exception): 
    pass

class TextResourceAdapter(TextResource, object):
    """
    """

    convertibles = ("TextResource", "BinaryResource", "WebResource")

    def __init__(self, client_resource):

        self._verify_compatibility(client_resource)
        self._client_resource = client_resource

    def read(self):

        if self._client_resource.__class__ is BinaryResource:
            return self._client_resource.read_plain_text()

        elif self._client_resource.__class__ is WebResource:
            return self._client_resource.read_json()

        return super(TextResourceAdapter, self).read()

    def _verify_compatibility(self, resource):

        if resource.__class__.__name__ not in self.__class__.convertibles:
            raise IncompatibleResourceError("{} cannot be adapted.".format(
                resource.__class__.__name__))


if __name__ == "__main__":

    client_resources = [BinaryResource(), WebResource(), TextResource()]

    for resource in client_resources:

        print("Adapting {} as a text resource...".format(
            resource.__class__.__name__))

        adapted_resource = TextResourceAdapter(resource)
        print(adapted_resource.read() + "\n")