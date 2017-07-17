""" The Observer Pattern

Notes:

The observer pattern can be used to model a one-to-many dependency
relationship between an object (the observable) and its dependents (the
observers). In this pattern, the observable is responsible for notifying all
observers of any relevant change in state. This is particularly useful when some
centralized state can affect de-centralized behaviour (such as distributed event
handling).

The following example simulates a forum (the observable, stateful entity) which
is observed by several natural language processing bots (the observers). Any
time a new post is added to the forum, the bots are notified. Each bot then
processes the new post and performs its responsibilities (the implementation of
the processing event is beyond the scope of this demo and thus left to your
imagination).

"""

class ObservableForum:
    """Represents a stateful entity (an online forum) that is aware of its
    observers (NLP bots). It is responsible for notifying the bots of any new
    posts (a relevant change in state).
    """

    def __init__(self): self._observer_bots = []

    def add_observer_bot(self, new_bot):
        """We assume that since every specific bot type represents a certain
        responsibility, only one instance of each type will be allowed to
        observe the forum. Therefore, only one instance of any child of
        AbstractObserverBot will be added to the list of observers.
        """

        if not any (isinstance(bot, new_bot.__class__) for bot in 
            self._observer_bots):
            print("Adding observer: {}".format(new_bot.__class__.__name__))
            self._observer_bots.append(new_bot)

    def remove_observer_bot(self, bot_to_remove):
        """Since there is only one instance of each observer bot type in the
        list, we remove the first type match we find.
        """

        for bot in self._observer_bots:
            if isinstance(bot, bot_to_remove.__class__):
                print("Removing observer: {}".format(bot.__class__.__name__))
                self._observer_bots.remove(bot)
                return None

    def new_post(self, post):
        """In a real case, this method might include more logic for handling a
        new post. Key to this pattern is that the observers are notified of the
        change in state (addition of the new post).
        """

        print("Adding post and notifying observers...")
        self._notify_observers(post)
        pass

    def _notify_observers(self, post):

        for bot in self._observer_bots:
            bot.process(post)

class AbstractObserverBot():
    """All observer bots inherit from this class. They all share a process
    method which the forum calls to notify them of a new post. We presume that
    each child will have a unique set of responsibilities when it comes to
    handling this event.
    """

    def process(self, post):
        """Called by the forum in the event of a new post."""

        print("> {} is processing the new post".format(self.__class__.__name__))

# This bot may be responsible for analysing the sentiment of the post.
class SentimentAnalyser(AbstractObserverBot): pass

# This bot may be responsible for detecting foul language and obfuscating it.
class ProfanityDetector(AbstractObserverBot): pass

# This bot may be responsible for detecting spam and blocking the post.
class SpamDetector(AbstractObserverBot): pass


if __name__ == "__main__":

    sa_bot = SentimentAnalyser()
    pd_bot = ProfanityDetector()
    sd_bot = SpamDetector()
    forum = ObservableForum()

    # Note how observers can be added/removed dynamically.
    forum.add_observer_bot(sa_bot)
    forum.add_observer_bot(pd_bot)
    forum.add_observer_bot(sd_bot)
    print("\n")

    forum.new_post("Hello this is a post.")
    print("\n")

    forum.remove_observer_bot(pd_bot)
    print("\n")

    forum.new_post("Hello this is another post.")
    print("\n")
