# This code is highly inspired by `srt.py` by Gyeongjae Choi.
# https://github.com/ryanking13/SRT/blob/master/SRT/srt.py


import requests
from .dataclass import Parameter, Passenger
from .constants import PassengerType, EMAIL_REGEX, PHONE_NUMBER_REGEX


SCHEME = 'https'
SR_HOST = 'app.srail.or.kr'
SR_PORT = '443'

SR_MOBILE = f'{SCHEME}://{SR_HOST}:{SR_PORT}'

SR_MAIN = f'{SR_MOBILE}/main/main.do'
SR_LOGIN = f'{SR_MOBILE}/apb/selectListApb01080_n.do'
SR_LOGOUT = f'{SR_MOBILE}/login/loginOut.do'
SR_SEARCH_SCHEDULE = f'{SR_MOBILE}/ara/selectListAra10007_n.do'
SR_RESERVE = f'{SR_MOBILE}/arc/selectListArc05013_n.do'
SR_TICKETS = f'{SR_MOBILE}/atc/selectListAtc14016_n.do'
SR_TICKET_INFO = f'{SR_MOBILE}/ard/selectListArd02017_n.do?'
SR_CANCEL = f'{SR_MOBILE}/ard/selectListArd02045_n.do'

DEFAULT_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Linux; Android 5.1.1; LGM-V300K Build/N2G47H) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36SRT-APP-Android V.1.0.6'
    ),
    'Accept': 'application/json',
}


class SR:
    def __init__(
            self,
            # parameter: Parameter | None = None,
            username: str | None = None,
            password: str | None = None,
            auto_login: bool = True,
            feedback: bool = False
        ) -> None:

        self.session = requests.session()
        self.session.headers.update(DEFAULT_HEADERS)

        # self.parameter = parameter
        self.username = username
        self.password = password
        self.feedback = feedback

        self.logged_in = False

        if auto_login and (not (username is None and password is None)):
            self.login()
        