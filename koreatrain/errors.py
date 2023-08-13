class KoreaTrainError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


class LoginError(KoreaTrainError):
    def __init__(self, msg: str = 'Login failed, please check platform, username, and password.'):
        super().__init__(msg)


class NotLoggedInError(KoreaTrainError):
    def __init__(self, msg: str = 'Not logged in.'):
        super().__init__(msg)


class SoldOutError(KoreaTrainError):
    def __init__(self, msg: str = 'The ticket is already sold out.'):
        super().__init__(msg)


class NoResultsError(KoreaTrainError):
    def __init__(self, msg: str = 'No result found.'):
        super().__init__(msg)


class ResponseError(KoreaTrainError):
    def __init__(self, msg: str):
        super().__init__(msg)
