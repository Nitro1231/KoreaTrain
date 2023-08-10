class KoreaTrainError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class KoreaTrainLoginError(KoreaTrainError):
    def __init__(self, msg='Login failed, please check platform, username, and password.'):
        super().__init__(msg)


class KoreaTrainNotLoginError(KoreaTrainError):
    def __init__(self):
        super().__init__('Not logged in.')
