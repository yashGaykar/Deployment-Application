
class AccountNameAlreadyExists(Exception):
    pass


class AccountDoesNotExists(Exception):
    pass


class KeyAlreadyExists(Exception):
    pass


class NoFileFoundException(Exception):
    pass


class AccountIdMissing(Exception):
    pass


class WrongCredentials(Exception):
    def __init__(self, message="Please Check Your AWS Credentials"):
        super(WrongCredentials, self).__init__(self)
        self.message = message

