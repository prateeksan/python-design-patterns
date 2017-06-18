"""The Flyweight Pattern

Notes:

If you work for a data science team or have to deal with big data, this pattern
will be particularly useful.

In situations wherein several objects have some common memory intensive state,
the flyweight pattern can be implemented to separate and store the memory
intensive state in a common shared object. In other words if object 'A' 
maintains data 'x' and 'y' as state, and object 'B' maintains data 'y' and 'z',
we can create a flyweight object 'C' which stores 'y'. Now 'A' and 'B' do
not need to maintain separate instances of 'y', they can both share the
flyweight's state.

The following implementation uses the pattern to build a module which can handle 
complex data requests with multiple queries to a database. Each ComplexRequest
accepts two kinds of queries - fresh data queries (FreshQuery) and historical
data queries (HistoricalQuery). Furthermore, it accepts a pointer to a cache for
historical queries. Assuming that historical data does not change, we have
implemented the HistoricalQuery class as a flyweight and the HistoricalDataCache
serves as shared state cache for the flyweight objects. A user can use this to
make complex queries that only query data which is fresh or previously not
fetched.

"""

class HistoricalDataCache:
    """Represents a local cache for historical data. It maps historical data to
    unique hashes of their query strings. This ensures only one db read is
    performed for each historical query.
    """

    # Implemented as a hash map (dict) shared by all instances of the class.
    _cache = {}

    def get(self, query_string):
        """Hashes the query string using the _query_hash method and checks the
        _cache's keys for the hash. If a key matching the has is found, its
        value (which contains a query object representing the result of the
        request) is returned to the caller. Else, the data is queried and
        the response object is cached and returned to the caller.
        """

        print("Checking cache for: {}".format(query_string))

        query_hash = self._query_hash(query_string)

        if not (query_hash in self.__class__._cache):
            print("\t{}".format(
                    "Query result not previously cached. Caching and returning."
                )
            )
            self.__class__._cache[query_hash] = HistoricalQuery(query_string)

        else:
            print("\t{}".format(
                    "Cached result found. Returning result from cache."
                )
            )

        return self.__class__._cache[query_hash]

    def _query_hash(self, query_string):
        """Creates a unique 10 digit integer hash of the query_string. This is
        used as the unique key for the query in the _cache.
        """

        return abs(hash(query_string)) % (10**10)


class Query:
    """Both fresh queries and historical queries share the same interface as
    defined here. This may be changed depending on the use case. The reason
    for using the FreshQuery and HistoricalQuery subclasses (defined below) is
    to clearly separate the two types of queries and letting the user know which
    queries are cacheable (or which have been returned from a cache).
    """

    def __init__(self, query_string):
        """The self.data attribute stores the memory intensive state that we are
        trying to manage. For this implementation, it makes sense to populate it
        during initialization.
        """

        self.query_string = query_string
        self.data = self.get_data()

    def get_data(self):
        """In a real use case, this would query the database and return a large
        object containing the requisite data.
        """

        return "Data for {}: {}".format(self.__class__.__name__, 
            self.query_string)

class FreshQuery(Query):
    pass

class HistoricalQuery(Query):
    pass

class ComplexRequest:
    """The end user of the module can use this to build complex data sets by
    making and aggregating multiple queries. This implementation is
    oversimplified for demonstrative purposes."""

    def __init__(self, historical_queries, fresh_queries, historical_cache):
        """During initialization, all requisite queries are separated into two
        types - historical and fresh queries. A pointer to the historical_cache
        is also stored since it will be used to process historical queries.
        """

        self.historical_queries = historical_queries
        self.fresh_queries = fresh_queries
        self.historical_cache = historical_cache

    def get(self):
        """In a real use case, this method would be responsible for establishing
        the relationship between fresh and historical data. This might involve
        merging, joining, pivoting or grouping the multiple data sets.
        """

        fresh_data = self._get_fresh_data()
        historical_data = self._get_historical_data()
        print("Merging the following data sets:")
        print("\t" + "\n\t".join(fresh_data))
        print("\t" + "\n\t".join(historical_data))

    def _get_fresh_data(self):
        """We assume that fresh data always needs to be queried from the db for
        each request.
        """

        fresh_data = []

        for query_string in self.fresh_queries:
            query = FreshQuery(query_string)
            fresh_data.append(query.data)

        return fresh_data

    def _get_historical_data(self):
        """This is where we can use the historical data cache and the power of
        the flyweight pattern to recycle previously queried historical data.
        """

        historical_data = []

        for query_string in self.historical_queries:
            query = self.historical_cache.get(query_string)
            historical_data.append(query.data)

        return historical_data


if __name__ == '__main__':
    """In this example, we make two complex requests that share a historical
    query to get all data from the archive_2 table. Therefore this query is only
    sent to the db once even though it is added to both requests.
    """

    historical_cache = HistoricalDataCache()

    request_1 = ComplexRequest(
        historical_queries=[
            "SELECT * FROM archive_1", 
            "SELECT * FROM archive_2"
        ],
        fresh_queries = [
            "SELECT * FROM live_1", 
            "SELECT * FROM live_2"
        ],
        historical_cache = historical_cache
    )
    print("> Making request_1...")
    data_1 = request_1.get()

    print("\n")

    print("> Making request_2...")
    request_2 = ComplexRequest(
        historical_queries=[
            "SELECT * FROM archive_2", 
            "SELECT * FROM archive_3"
        ],
        fresh_queries = [
            "SELECT * FROM live_1", 
            "SELECT * FROM live_2"
        ],
        historical_cache = historical_cache
    )
    data_2 = request_2.get()

