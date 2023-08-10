from SRT import *
from korail2 import *

from .tools import get_time
from .constants import Platform
from .dataclass import Parameter, SRParameter, KorailParameter


class KoreaTrain:
    def __init__(
            self,
            platform: Platform,
            parameter: Parameter | None = None,
            username: str | None = None,
            password: str | None = None,
            auto_login: bool = True,
            feedback: bool = False
        ) -> None:

        self.platform = platform
        self.parameter = parameter
        self.username = username
        self.password = password

        self.logged_in = False
        self.service = None

        if parameter is not None and not isinstance(parameter, Parameter):
            raise ValueError('Invalid parameter.')

        if username is None and password is None:
            auto_login = False

        match platform:
            case Platform.SR:
                self.service = SRT(username, password, False, feedback)
            case Platform.KORAIL:
                self.service = Korail(username, password, False, feedback)
            case _:
                raise ValueError('Invalid platform.')

        if auto_login: self.login()


    def __repr__(self) -> str:
        return f'[{type(self).__name__}] platform: {self.platform}, parameter: {self.parameter}, logged_in: {self.logged_in}.'


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


    def set_parameter(self, parameter: Parameter):
        if isinstance(parameter, Parameter): # Check if the base class of the parameter is the Parameter.
            self.parameter = parameter
        else:
            raise ValueError('Invalid parameter.')


    def search_train(self, parameter: Parameter | None = None, available_only: bool = True) -> list:
        if parameter is None:
            parameter = self.parameter
        if parameter is None or not isinstance(parameter, Parameter):
            raise ValueError('Invalid parameter.')

        match self.platform:
            case Platform.SR:
                if type(parameter) is not SRParameter:
                    raise ValueError('Invalid parameter.')
                return self.service.search_train(
                    dep=parameter.dep,
                    arr=parameter.arr,
                    date=parameter.date,
                    time=parameter.time,
                    time_limit=parameter.time_limit,
                    available_only=available_only
                )

            case Platform.KORAIL:
                if type(parameter) is not KorailParameter:
                    raise ValueError('Invalid parameter.')
                
                # TODO: Optimize this by calling multiple search_train instead of calling the search_train_allday.
                trains = self.service.search_train_allday(
                    dep=parameter.dep,
                    arr=parameter.arr,
                    date=parameter.date,
                    time=parameter.time,
                    train_type=parameter.train_type,
                    passengers=parameter.passengers,
                    include_no_seats=(not available_only)
                )

                if parameter.time is None: parameter.time = get_time()
                if parameter.time_limit is None:
                    return trains
                else:
                    return [train for train in trains if int(parameter.time) <= int(train.dep_time) <= int(parameter.time_limit)]

            case _:
                raise ValueError('Invalid platform.')


    def reserve(self, train, parameter: Parameter | None = None):
        if parameter is None:
            parameter = self.parameter
        if parameter is None or not isinstance(parameter, Parameter):
            raise ValueError('Invalid parameter.')

        match self.platform:
            case Platform.SR:
                if type(parameter) is not SRParameter:
                    raise ValueError('Invalid parameter.')
                return self.service.reserve(
                    train=train,
                    passengers=parameter.passengers,
                    special_seat=parameter.reserve_option,
                    window_seat=parameter.window
                )

            case Platform.KORAIL:
                if type(parameter) is not KorailParameter:
                    raise ValueError('Invalid parameter.')
                return self.service.reserve(
                    train=train,
                    passengers=parameter.passengers,
                    option=parameter.reserve_option
                )

            case _:
                raise ValueError('Invalid platform.')


    def get_reservations(self, paid_only: bool = False) -> list:
        # TODO: paid_only option only works for SR. Implement one for Korail.
        match self.platform:
            case Platform.SR:
                return self.service.get_reservations(paid_only)

            case Platform.KORAIL:
                return self.service.reservations()

            case _:
                raise ValueError('Invalid platform.')


    # def get_tickets(self):
    #     pass


    def cancel(self, reservation) -> bool:
        return self.service.cancel(reservation)
