""" The Composite Pattern

Notes:

"""

class DataObject():

    def read(self):
        pass

class DataNode(DataObject):

    def __init__(self, data):
        self._data = data

    def read(self):
        print("Node Data: {}".format(self._data))

class DataComposite(DataObject):

    def __init__(self, data):
        self._meta_data = data
        self.sub_objects = []

    def read(self):
        print("Data Composite For: {}".format(self._meta_data))
        for data_object in self.sub_objects:
            data_object.read()

    def add(self, data_object):
        self.sub_objects.append(data_object)

    def remove(self, data_object):
        self.sub_objects.remove(data_object)


if __name__ == "__main__":

    python = DataNode("Python")
    ruby = DataNode("Ruby")

    english = DataNode("English")
    french = DataNode("French")

    lang_tree = DataComposite("Languages")
    programming_lang_tree = DataComposite("Programming Languages")
    human_lang_tree = DataComposite("Human Languages")

    programming_lang_tree.add(python)
    programming_lang_tree.add(ruby)

    human_lang_tree.add(english)
    human_lang_tree.add(french)

    lang_tree.add(human_lang_tree)
    lang_tree.add(programming_lang_tree)

    lang_tree.read()


