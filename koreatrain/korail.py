# This code is highly inspired by `korail2.py` by Taehoon Kim.
# https://github.com/carpedm20/korail2/blob/master/korail2/korail2.py


import json
import requests
from functools import reduce
from .dataclass import Parameter, Passenger
from .constants import PassengerType, EMAIL_REGEX, PHONE_NUMBER_REGEX
from .errors import KoreaTrainError, LoginError, NotLoggedInError, SoldOutError, NoResultsError, ResponseError


SCHEME = 'https'
KORAIL_HOST = 'smart.letskorail.com'
KORAIL_PORT = '443'

KORAIL_DOMAIN = f'{SCHEME}://{KORAIL_HOST}:{KORAIL_PORT}'
KORAIL_MOBILE = f'{KORAIL_DOMAIN}/classes/com.korail.mobile'

KORAIL_LOGIN = f'{KORAIL_MOBILE}.login.Login'
KORAIL_LOGOUT = f'{KORAIL_MOBILE}.common.logout'
KORAIL_SEARCH_SCHEDULE = f'{KORAIL_MOBILE}.seatMovie.ScheduleView'
KORAIL_TICKETRESERVATION = f'{KORAIL_MOBILE}.certification.TicketReservation'
KORAIL_REFUND = f'{KORAIL_MOBILE}.refunds.RefundsRequest'
KORAIL_MYTICKETLIST = f'{KORAIL_MOBILE}.myTicket.MyTicketList'
KORAIL_MYTICKET_SEAT = f'{KORAIL_MOBILE}.refunds.SelTicketInfo'

KORAIL_MYRESERVATIONLIST = f'{KORAIL_MOBILE}.reservation.ReservationView'
KORAIL_CANCEL = f'{KORAIL_MOBILE}.reservationCancel.ReservationCancelChk'

KORAIL_STATION_DB = f'{KORAIL_MOBILE}.common.stationinfo?device=ip'
KORAIL_STATION_DB_DATA = f'{KORAIL_MOBILE}.common.stationdata'
KORAIL_EVENT = f'{KORAIL_MOBILE}.common.event'
KORAIL_PAYMENT = f'{KORAIL_DOMAIN}/ebizmw/PrdPkgMainList.do'
KORAIL_PAYMENT_VOUCHER = f'{KORAIL_DOMAIN}/ebizmw/PrdPkgBoucherView.do'

DEFAULT_HEADERS = {
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Nexus 4 Build/LMY48T)'
}

DEVICE = 'AD'
KORAIL_VER = '190617001'

RESULT_SUCCESS = 'SUCC'
RESULT_FAIL = 'FAIL'


class Korail:
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
            login_type = '5'
        elif PHONE_NUMBER_REGEX.match(self.username):
            login_type = '4'
        else:
            login_type = '2'

        data = {
            'Device': DEVICE,
            # 'Version': '150718001',
            'txtInputFlg': login_type,
            'txtMemberNo': self.username,
            'txtPwd': self.password
        }
        res = self.session.post(KORAIL_LOGIN, data=data)
        json_data = json.loads(res.text)
        self._log(json_data)

        if json_data['strResult'] == RESULT_SUCCESS and json_data.get('strMbCrdNo') is not None:
            self.key = json_data['Key']
            # self.membership_number = j['strMbCrdNo']
            # self.name = j['strCustNm']
            # self.email = j['strEmailAdr']
            self.logged_in = True
            return True
        else:
            self.logged_in = False
            # raise LoginError(json_data['h_msg_txt'])
            return False


    def logout(self) -> bool:
        res = self.session.get(KORAIL_LOGOUT)
        self._log(res.text.strip())
        self.logged_in = False
        return True


    def search_train(self, parameter: Parameter | None = None, available_only: bool = True) -> list:
        def count(passengers: list[Passenger], passenger_type: PassengerType) -> int:
            return reduce(lambda x, y: x + y.count, list(filter(lambda x: x.type_code == passenger_type, passengers)), 0)

        data = {
            'Device': DEVICE,
            'Version': KORAIL_VER,
            'txtGoStart': parameter.dep,
            'txtGoEnd': parameter.arr,
            'txtGoAbrdDt': parameter.date,
            'txtGoHour': parameter.time,
            'selGoTrain': parameter.train_type.value,
            'txtTrnGpCd': parameter.train_type.value,
            'txtPsgFlg_1': count(parameter.passengers, PassengerType.ADULT),                # 어른 - 만 13세 이상
            'txtPsgFlg_2': count(parameter.passengers, PassengerType.CHILD),                # 어린이 - 만 6세 ~ 12세 어린이
            'txtPsgFlg_8': count(parameter.passengers, PassengerType.CHILD_UNDER_6),        # 유아 - 만 6세 미만 유아
            'txtPsgFlg_3': count(parameter.passengers, PassengerType.SENIOR),               # 경로 - 만 65세 이상 경로
            'txtPsgFlg_4': count(parameter.passengers, PassengerType.DISABILITY_1_TO_3),    # 중증 - 장애의 정도가 심한 장애인(구1~3급)
            'txtPsgFlg_5': count(parameter.passengers, PassengerType.DISABILITY_4_TO_6),    # 경증 - 장애의 정도가 심한 장애인(구1~3급)
            'txtSeatAttCd_2': parameter.heading.value,
            'txtSeatAttCd_3': parameter.seat_location.value,
            'txtSeatAttCd_4': parameter.seat_type.value,
            'radJobId': '1',
            # 'txtCardPsgCnt': '0',
            # 'txtGdNo': '',
            # 'txtJobDv': '',
            # 'txtMenuId': '11',
        }
        self._log(data)
        res = self.session.get(KORAIL_SEARCH_SCHEDULE, params=data)
        json_data = json.loads(res.text)
        self._log(json_data)

        if self._result_check(json_data):
            train_infos = json_data['trn_infos']['trn_info']
            print(train_infos)
            # 여기부터


    def _log(self, msg: str) -> None:
        if self.feedback:
            print('[*Korail]', msg)


    def _result_check(self, json_data: dict):
        text = json_data['h_msg_txt']

        if self.feedback:
            self._log(text)

        if json_data['strResult'] == RESULT_FAIL:
            code = json_data['h_msg_cd']

            match code:
                case 'P058':
                    raise NotLoggedInError()
                case 'P100' | 'WRG000000' | 'WRD000061' | 'WRT300005':
                    raise NoResultsError()
                case 'ERR211161':
                    raise SoldOutError()
                case _:
                    raise ResponseError(f'An unknown error occurred. (message: {text}, code: {code})')
        else:
            return True
