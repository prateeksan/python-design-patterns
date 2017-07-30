class ErrorMeta(type):

    registry = {}

    def __new__(cls, *args, **kwargs):

        new_error_type = type.__new__(cls, *args, **kwargs)
        cls.registry[new_error_type.code] = new_error_type
        return new_error_type

class BaseError:
    __metaclass__ = ErrorMeta
    code = 999

if __name__ == "__main__":

    print("Registry with only the BaseError implemented:")
    print(ErrorMeta.registry)

    class ClientError(BaseError):
        code = 400

    class ServerError(BaseError):
        code = 500

    print("\nRegistry with client and server errors implemented:")
    print(ErrorMeta.registry)
