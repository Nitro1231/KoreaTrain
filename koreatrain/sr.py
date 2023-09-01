# This code is highly inspired by `srt.py` by Gyeongjae Choi.
# https://github.com/ryanking13/SRT/blob/master/SRT/srt.py


import json
import requests
from functools import reduce
from .station import search_station, STATION_CODE
from .dataclass import Parameter, Passenger
from .constants import PassengerType, EMAIL_REGEX, PHONE_NUMBER_REGEX
from .errors import LoginError
from .tools import count


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
        res = self.session.post(SR_LOGOUT)
        self._log(res.text.strip())
        self.logged_in = False
        return True


    def search_train(self, parameter: Parameter | None = None, available_only: bool = True) -> list:
        if parameter.dep not in STATION_CODE:
            raise ValueError(f'Station "{parameter.dep}" not exists. Did you mean: {search_station(parameter.dep, 1)}?')
        if parameter.arr not in STATION_CODE:
            raise ValueError(f'Station "{parameter.dep}" not exists. Did you mean: {search_station(parameter.dep, 1)}?')

        dep_code = STATION_CODE[parameter.dep]
        arr_code = STATION_CODE[parameter.arr]

        data = {
            'chtnDvCd': '1',
            'stlbTrnClsfCd': '05',
            'dptRsStnCdNm': parameter.dep,
            'arvRsStnCdNm': parameter.arr,
            'dptRsStnCd': dep_code,
            'arvRsStnCd': arr_code,
            'dptDt': parameter.date,
            'dptTm': parameter.time,
            'psgNum': reduce(lambda x, y: x + y.count, parameter.passengers, 0),                        # Total count
            'psgInfoPerPrnb1': count(parameter.passengers, PassengerType.ADULT),                  # 어른 - 만 13세 이상
            'psgInfoPerPrnb5': count(parameter.passengers, PassengerType.CHILD),                  # 어린이 - 만 6세 ~ 12세 어린이
            'psgInfoPerPrnb4': count(parameter.passengers, PassengerType.SENIOR),                 # 경로 - 만 65세 이상 경로
            'psgInfoPerPrnb2': count(parameter.passengers, PassengerType.DISABILITY_1_TO_3),      # 중증 - 장애의 정도가 심한 장애인(구1~3급)
            'psgInfoPerPrnb3': count(parameter.passengers, PassengerType.DISABILITY_4_TO_6),      # 경증 - 장애의 정도가 심하지 않은 장애인(구4~6급)
            'locSeatAttCd1': parameter.seat_location.value,
            'rqSeatAttCd1': parameter.seat_type.value,
            'trnGpCd': '300',
            'dlayTnumAplFlg': 'Y',
            'seatAttCd': '015',
            'isRequest': 'Y'
        }
        self._log(data)
        res = self.session.post(SR_SEARCH_SCHEDULE, data=data)
        self._log(res.text)


    def _log(self, *msg: str) -> None:
        if self.feedback:
            print('[*SR]', *msg)


    def _parse_data(self, response: str):
        pass
