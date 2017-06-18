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

"""

class HistoricalDataCache:

    _cache = {}

    def get(self, query_string):

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
        return abs(hash(query_string)) % (10**10)


class Query:

    def __init__(self, query_string):
        self.query_string = query_string
        self.data = self.get_data()

    def get_data(self):
        return "Data for {}: {}".format(self.__class__.__name__, 
            self.query_string)

class FreshQuery(Query):
    pass

class HistoricalQuery(Query):
    pass

class ComplexRequest:
    def __init__(self, historical_queries, fresh_queries, historical_cache):
        self.historical_queries = historical_queries
        self.fresh_queries = fresh_queries
        self.historical_cache = historical_cache

    def _get_fresh_data(self):

        fresh_data = []

        for query_string in self.fresh_queries:
            query = FreshQuery(query_string)
            fresh_data.append(query.data)

        return fresh_data

    def _get_historical_data(self):

        historical_data = []

        for query_string in self.historical_queries:
            query = self.historical_cache.get(query_string)
            historical_data.append(query.data)

        return historical_data

    def get(self):
        fresh_data = self._get_fresh_data()
        historical_data = self._get_historical_data()
        print("Merging the following data sets:")
        print("\t" + "\n\t".join(fresh_data))
        print("\t" + "\n\t".join(historical_data))

if __name__ == '__main__':

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

