# This code is highly inspired by `srt.py` by Gyeongjae Choi.
# https://github.com/ryanking13/SRT/blob/master/SRT/srt.py


import json
import requests
from .dataclass import Parameter, Passenger
from .constants import PassengerType, EMAIL_REGEX, PHONE_NUMBER_REGEX
from .errors import LoginError


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

RESULT_SUCCESS = 'SUCC'
RESULT_FAIL = 'FAIL'


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


    def login(self, username: str | None = None, password: str | None = None) -> bool:
        if username is not None: self.username = username
        if password is not None: self.password = password
        if self.username is None or self.password is None:
            raise TypeError('The username or password cannot be None type.')

        if EMAIL_REGEX.match(self.username):
            login_type = '2'
        elif PHONE_NUMBER_REGEX.match(self.username):
            login_type = '3'
            self.username = self.username.replace('-', '')
        else:
            login_type = '1'

        data = {
            'auto': 'Y',
            'check': 'Y',
            'page': 'menu',
            'deviceKey': '-',
            'customerYn': '',
            'login_referer': SR_MAIN,
            'srchDvCd': login_type,
            'srchDvNm': self.username,
            'hmpgPwdCphd': self.password,
        }
        res = self.session.post(SR_LOGIN, data=data)
        json_data = json.loads(res.text)
        self._log(json_data)

        if json_data.get('strResult') == RESULT_FAIL:
            self.logged_in = False
            # raise LoginError(json_data['MSG'])
            return False
        else:
            self.logged_in = True
            return True


    def logout(self) -> bool:
        res = self.session.get(SR_LOGOUT)
        self._log(res.text.strip())
        self.logged_in = False
        return True


    def _log(self, msg: str) -> None:
        if self.feedback:
            print('[*SR]', msg)
