""" The Decorator Pattern

Notes:


"""

def validate_inputs(decorators):

    def decorate(cls):
        for method in dir(cls):
            if callable(getattr(cls, method)) and \
                method.startswith("input_"):
                for decorator in reversed(decorators):
                    setattr(cls, method, decorator(getattr(cls, method)))
        return cls
    return decorate

def is_string(func):
    def wrapper(self, text):
        if type(text) is not str:
            return "'{}' is invalid. Input should be a string.".format(text)
        return func(self, text)
    return wrapper

def is_lowercase(func):
    def wrapper(self, text):
        if not text.islower():
            return "'{}' is invalid. Input should be lowercase.".format(text)
        return func(self, text)  
    return wrapper

@validate_inputs([is_string, is_lowercase])
class TextForm():

    def input_username(self, name): 
        return  "'{}' is valid. Input registered.".format(name)

    def input_team_name(self, team):
        return "'{}' is valid. Input registered.".format(team)

    def special_input_comments(self, comments):
        return "Comments are always valid!"

if __name__ == "__main__":
    form = TextForm()

    print("Attempting to input username:")
    print(form.input_username("Bob"))
    print(form.input_username(808))
    print(form.input_username("bob"))
    print(form.input_team_name(2.1))

    print("\n" + "Attempting to input team name:")
    print(form.input_team_name("BobRockers"))
    print(form.input_team_name("bobrockers"))

    print("\n" + "Attempting to input comments:")
    print(form.special_input_comments("THIS IS ALL UPPERCASE"))

    print("\n")