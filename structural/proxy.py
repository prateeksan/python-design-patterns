""" The Proxy Pattern

Notes:

As the name suggests, the pattern involves creating a proxy or an intermediary
interface between an object or service and its user. The proxy allows the user
to access the object or service through it, while adding the possibility to
wrap calls with additional functionality. This pattern is particularly useful in
situations where intercepting a call can create meaningful optimizations
(caching/queuing) or add security (authentication/sanitization).

This example simulates the process of sending a request to interact with a
resource on a server via a proxy. The proxy implemented here stores a pointer to
a cached version of the resource. For read requests, it checks the cache before
pinging the server. It also handles updating the cache for writes and fresh
reads.

"""

class ServerResource:
    """This class provides an interface to read and write to a resource on a
    server. It does not need to have knowledge of the proxy but we assume that
    one can access it only via the proxy (for the caching model to work).
    """

    def read(self, query):
        print("\t" + "Reading from {}...".format(self.__class__.__name__))
        pass

    def write(self, data):
        print("\t" + "Writing to {}...".format(self.__class__.__name__))
        pass

class CachedResource(ServerResource):
    """The cached resource shares the same interface as the server's resource.
    It is essentially a clone of the original resource that should be up to date
    with original.
    """
    pass

class Proxy:
    """Any request to read or write to a resource on the server passes through
    this proxy. While the interface is identical to the ServerResource in
    this example, I have purposefully avoided creating an inheritance
    relationship between the two. This is because the proxy need not provide an
    interface to only one resource. Furthermore, it need not be an exact
    representation of the original resource. Having said that, it does need to
    allow the user to indirectly access the original resource.
    """

    def __init__(self):
        """Upon initializing, the proxy connects to both the server and the
        cache.
        """

        self._resource = ServerResource()
        self._cache = CachedResource()

    def read(self, query):
        """Read requests are first sent to the cache. If the response was
        previously cached, it is returned from the cache. Otherwise, the request
        is sent to the server and the response is fed into the cache and sent
        back to the user.
        """

        cached_result = self._cache.read(query)
        if cached_result:
            print("\t" + "Returning data from cache...")
            return cached_result

        print("\t" + "No cached data found...")
        server_result = self._resource.read(query)
        self._cache.write(server_result)

        print("\t" + "Returning data from server...")
        return server_result

    def write(self, data):
        """Write requests immediately update the cache and then update the
        server's resource. Finally, the response from the server is returned to
        the user."""
 
        self._cache.write(data)
        return self._resource.write(data)

if __name__ == "__main__":

    proxy = Proxy()

    print("Making Read Query:")
    proxy.read("Sample Query String")
    print("\n")

    print("Making Write Query:")
    proxy.write("Sample Data")
    print("\n")


