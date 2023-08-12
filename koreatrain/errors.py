class KoreaTrainError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class LoginError(KoreaTrainError):
    def __init__(self, msg='Login failed, please check platform, username, and password.'):
        super().__init__(msg)


class NotLoggedInError(KoreaTrainError):
    def __init__(self):
        super().__init__('Not logged in.')
