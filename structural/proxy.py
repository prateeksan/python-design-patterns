""" The Proxy Pattern

Notes:



"""

class ServerResource:

    def read(self, query):
        print("\t" + "Reading from {}...".format(self.__class__.__name__))
        pass

    def write(self, data):
        print("\t" + "Writing to {}...".format(self.__class__.__name__))
        pass

class CachedResource(ServerResource):
    pass

class Proxy:

    def __init__(self):
        self._resource = ServerResource()
        self._cache = CachedResource()

    def read(self, query):

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


