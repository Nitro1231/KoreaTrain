from SRT import *
from korail2 import *

from .constants import Platform


class KoreaTrain:
    def __init__(self, platform: Platform, username: str | None = None, password: str | None = None, auto_login: bool = True, feedback: bool = False) -> None:
        self.platform = platform
        self.username = username
        self.password = password
        self.logged_in = False
        self.service = None

        if username is None and password is None:
            auto_login = False

        match platform:
            case Platform.SR:
                self.service = SRT(auto_login=auto_login, verbose=feedback)
            case Platform.KORAIL:
                self.service = Korail(auto_login=auto_login, want_feedback=feedback)
            case _:
                raise ValueError

        if auto_login: self.login()


    def __repr__(self) -> str:
        return f'[KoreaTrain] Platform: {self.platform}, login? {self.logged_in}.'


    def login(self, username: str | None = None, password: str | None = None) -> bool:
        if username is None: username = self.username
        if password is None: password = self.password
        if username is None or password is None:
            raise ValueError('Invalid login information')

        self.logged_in = self.service.login(username, password)
        return self.logged_in


    def logout(self) -> bool:
        self.service.logout()
        return True
