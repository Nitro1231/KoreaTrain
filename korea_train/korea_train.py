from SRT import *
from korail2 import *

from .constants import Platform
from .dataclass import Search, SRSearch, KorailSearch


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
                self.service = SRT(username, password, False, feedback)
            case Platform.KORAIL:
                self.service = Korail(username, password, False, feedback)
            case _:
                raise ValueError

        if auto_login: self.login()


    def __repr__(self) -> str:
        return f'[{type(self).__name__}] platform: {self.platform}, logged_in: {self.logged_in}.'


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


    def search_train(self, param: Search, available_only: bool = True) -> list:
        match self.platform:
            case Platform.SR:
                if type(param) != SRSearch:
                    raise ValueError('Mismatched param type.')
                return self.service.search_train(
                    dep=param.dep,
                    arr=param.arr,
                    date=param.date,
                    time=param.time,
                    time_limit=param.time_limit,
                    available_only=available_only
                )

            case Platform.KORAIL:
                if type(param) != KorailSearch:
                    raise ValueError('Mismatched param type.')
                trains = self.service.search_train_allday(
                    dep=param.dep,
                    arr=param.arr,
                    date=param.date,
                    time=param.time,
                    train_type=param.train_type,
                    passengers=param.passengers,
                    include_no_seats=(not available_only)
                )

                if param.time is None: param.time = '000000'
                if param.time_limit is None:
                    return trains
                else:
                    return [train for train in trains if int(param.time) <= int(train.dep_time) <= int(param.time_limit)]

            case _:
                raise ValueError('Invalid search parameters.')


    def reserve(self):
        pass


    def tickets(self):
        pass


    def reservations(self):
        pass


    def cancel(self):
        pass
