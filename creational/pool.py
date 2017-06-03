""" The Pool Pattern

Notes:

As the name suggests, the pool pattern involves creating and maintaining a pool
of re-usable objects which may possess independent states. The pool itself boils
down to being an iterable which can be implemented in any manner that suits your
use-case. They key is to minimize the number of object instantiations. This
pattern is useful when:

+ Constructing new objects is expensive (time complexity/ space complexity/
    bandwidth)
+ Objects need to be put in and out of use very frequently but there is no need
    for unique objects per use.
+ Only a small amount of instances are in use at any given time.

The following implementation shows how to create a simple worker pool with
an interface to activate/deactivate workers and manage the size of the pool.
Note that the functionality of the workers themselves have not been implemented
since it is not pertinent to the pattern.

"""

class WorkerPoolError(Exception):
    """A base error class for all errors in this module. While this is not
    pertinent to the pattern, its always good to have a base error class if your
    module implements custom errors (for testing/error-handling etc.).
    """
    pass

class OverLimitError(WorkerPoolError):
    """Raised when too many workers are created."""
    pass

class WorkerBusyError(WorkerPoolError):
    """Raised to prevent unwarranted interactions with a busy worker."""
    pass

class Worker:
    """Represents the worker object. Its implementation is beyond the scope of
    this demo but it could built in a manner with internal state and other
    properties.
    """
    pass

class WorkerPool:
    """The pool object is at the core of this design pattern. Depending on your
    needs, it may be useful to implement this as a singleton. The WorkerPool
    object controls the creation and deletion of workers in a manner that is
    optimized to meet the use-case of this pattern (see 'Notes').
    """

    # A constant that limits max workers in the pool.
    limit = 8

    def __init__(self, count):
        """The constructor in this example accpets a worker count and initializes
        that many workers (as long as it is below the limit). For more complex
        cases with time-consuming object creations, it may make sense to separate
        the logic to initializes the workers in the pool from this constructor.
        """

        self.within_limit_check(count)
        self._workers = [Worker() for n in range(count)]
        self.active_count = 0

    def within_limit_check(self, count):
        """Helper function to check if the worker count is within limit."""

        if count > WorkerPool.limit or count <= 0:
            raise OverLimitError("Valid Worker Count Range: 0 - {}".format(
                WorkerPool.limit
            ))

        return True

    def activate_worker(self):
        """Note that when a worker is activated, it is removed from the _workers
        list. However the pool maintains a list of active workers. Presuming that
        constucting new worker objects is costly, this can be very useful.
        """

        self.active_count += 1
        return self._workers.pop()

    def deactivate_worker(self, worker):
        """When a worker is deactivated, it is returned to the _workers list. If
        the worker object maintained internal state, this would be a good place
        to reset it (or set it to a default, dormant state).
        """

        self.active_count -=1
        self._workers.append(worker)

    def resize(self, new_count):
        """In case an active worker pool needs to be resized, the ideal solution
        would be to perform the resize without deleting any workers that need to
        be recreated immediately after. This method demonstrates one way of
        handling this while also ensuring that the resized count is within limit
        and the process does not disrupt active workers.
        """

        self.within_limit_check(new_count)
        total_workers = len(self._workers) + self.active_count

        diff = new_count - total_workers

        if diff == 0:
            pass
        elif diff > 0:
            for n in range(diff):
                self._workers.append(Worker())
        elif diff < 0:
            if diff > len(self._workers):
                raise WorkerBusyError("Can't resize due to busy workers.")
            else:
                for n in range(abs(diff)):
                    self._workers.pop()


if __name__ == "__main__":

    print("Creating worker pool with 4 workers...")
    worker_pool = WorkerPool(4)

    print("\nActivating 2 workers...")
    worker_1 = worker_pool.activate_worker()
    worker_2 = worker_pool.activate_worker()

    print("\nDeactivating 1 worker...")
    worker_pool.deactivate_worker(worker_2)

    print("1 Worker Active: {}".format(worker_pool.active_count == 1))

    print("\nRe-sizing pool to 7 workers...")
    worker_pool.resize(7)

    print("7 Total Workers: {}".format(
        len(worker_pool._workers) + worker_pool.active_count == 7
    ))

    print("\nRe-sizing pool to 6 workers...")
    worker_pool.resize(6)

    print("Total Workers: {}".format(
        len(worker_pool._workers) + worker_pool.active_count == 6
    ))
    print("1 Worker Still Active: {}".format(worker_pool.active_count == 1))

    print("\n")

