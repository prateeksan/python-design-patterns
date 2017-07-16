""" The Observer Pattern

Notes:



"""

class ObservableForum:

    def __init__(self):
        self._observer_bots = []

    def add_observer_bot(self, new_bot):

        if not any (isinstance(bot, new_bot.__class__) for bot in 
            self._observer_bots):
            print("Adding observer: {}".format(new_bot.__class__.__name__))
            self._observer_bots.append(new_bot)

    def remove_observer_bot(self, bot_to_remove):
        for bot in self._observer_bots:
            if isinstance(bot, bot_to_remove.__class__):
                print("Removing observer: {}".format(bot.__class__.__name__))
                self._observer_bots.remove(bot)

    def new_post(self, post):
        print("Adding post and notifying observers...")
        self._notify_observers(post)
        pass

    def _notify_observers(self, post):
        for bot in self._observer_bots:
            bot.process(post)

class ObserverBot():
 
    def process(self, post):
        print("> {} is processing the new post".format(self.__class__.__name__))

class SentimentAnalyser(ObserverBot): pass

class ProfanityDetector(ObserverBot): pass

class SpamDetector(ObserverBot): pass


if __name__ == "__main__":

    sa_bot = SentimentAnalyser()
    pd_bot = ProfanityDetector()
    sd_bot = SpamDetector()
    forum = ObservableForum()

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
