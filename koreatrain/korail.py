# This code is highly inspired by `korail2.py` by Taehoon Kim.
# https://github.com/carpedm20/korail2/blob/master/korail2/korail2.py


import json
import requests
import logging as log
from datetime import datetime, timedelta
from .dataclass import Parameter, Passenger, KorailTrain
from .constants import PassengerType, EMAIL_REGEX, PHONE_NUMBER_REGEX
from .errors import KoreaTrainError, LoginError, NotLoggedInError, SoldOutError, NoResultsError, ResponseError
from .tools import count, save_json, _code_logger


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
        log.info(json_data)

        if json_data['strResult'] == RESULT_SUCCESS and json_data.get('strMbCrdNo') is not None:
            self.key = json_data['Key']
            self.logged_in = True
            return True
        else:
            self.logged_in = False
            log.warning(json_data['h_msg_txt'])
            return False


    def logout(self) -> bool:
        res = self.session.get(KORAIL_LOGOUT)
        log.info(res.text.strip())
        self.logged_in = False
        return True


    def search_train(self, parameter: Parameter | None = None, available_only: bool = True) -> list:
        data = {
            'Device': DEVICE,
            'Version': KORAIL_VER,
            'txtGoStart': parameter.dep,
            'txtGoEnd': parameter.arr,
            'txtGoAbrdDt': parameter.date,
            'txtGoHour': parameter.time,
            'selGoTrain': parameter.train_type.value,
            'txtTrnGpCd': parameter.train_type.value,
            'txtPsgFlg_1': count(parameter.passengers, PassengerType.ADULT),                    # 어른 - 만 13세 이상
            'txtPsgFlg_2': count(parameter.passengers, PassengerType.CHILD),                    # 어린이 - 만 6세 ~ 12세 어린이
            'txtPsgFlg_8': count(parameter.passengers, PassengerType.CHILD_UNDER_6),            # 유아 - 만 6세 미만 유아
            'txtPsgFlg_3': count(parameter.passengers, PassengerType.SENIOR),                   # 경로 - 만 65세 이상 경로
            'txtPsgFlg_4': count(parameter.passengers, PassengerType.DISABILITY_1_TO_3),        # 중증 - 장애의 정도가 심한 장애인(구1~3급)
            'txtPsgFlg_5': count(parameter.passengers, PassengerType.DISABILITY_4_TO_6),        # 경증 - 장애의 정도가 심하지 않은 장애인(구4~6급)
            'txtSeatAttCd_2': parameter.heading.value,
            'txtSeatAttCd_3': parameter.seat_location.value,
            'txtSeatAttCd_4': parameter.seat_type.value,
            'radJobId': '1',
            # 'txtCardPsgCnt': '0',
            # 'txtGdNo': '',
            # 'txtJobDv': '',
            # 'txtMenuId': '11',
        }
        trains = list()
        upper_time_limit = int(parameter.time_limit)
        while True:
            log.debug('Requesting train info...')
            log.debug(data)
            res = self.session.post(KORAIL_SEARCH_SCHEDULE, data=data)
            json_data = json.loads(res.text)

            try:
                assert self._result_check(json_data) # assert True
            except NoResultsError: # No more data
                log.debug('=' * 20 + '[Korail / End Point - No more data]' + '=' * 20)
                break

            for info in json_data['trn_infos']['trn_info']:
                train = KorailTrain(info)
                last_dep_time = train.dep_time

                if int(train.dep_time) < upper_time_limit:
                    if available_only and not train.seat_available():
                        continue
                    trains.append(train)
                else:
                    log.debug('=' * 20 + '[Korail / End Point - Reach time limit]' + '=' * 20)
                    break

            next_dep_time = datetime.strptime(last_dep_time, '%H%M%S') + timedelta(seconds=1)
            data['txtGoHour'] = next_dep_time.strftime('%H%M%S')

        log.debug(str(trains).replace(', [', ',\n['))
        return trains


    def reserve(self, parameter: Parameter, train: KorailTrain):
        pass


    def get_reservations(self, paid_only: bool = False):
        if not self.logged_in:
            raise NotLoggedInError()

        data = {
            'Device': DEVICE,
            'Version': KORAIL_VER,
            'Key': self.key,
        }
        res = self.session.post(KORAIL_MYRESERVATIONLIST, data=data)
        json_data = json.loads(res.text)
        log.debug(json_data)
        self._result_check(json_data)


    def _result_check(self, json_data: dict):
        result = json_data['strResult']
        code = json_data['h_msg_cd']
        message = json_data['h_msg_txt']
        log.debug('Korail result check: ' + str(json_data))
        _code_logger('korail', result, code, message)

        if self.feedback:
            log.info(message)

        match code:
            case 'IRZ000001': # Login success.
                return True
            case 'S034' | 'P058': # Login failed.
                raise NotLoggedInError()
            case 'P100' | 'WRG000000' | 'WRD000061' | 'WRT300005':
                raise NoResultsError()
            case 'ERR211161':
                raise SoldOutError()
            case _:
                if result == RESULT_SUCCESS:
                    return True
                elif result == RESULT_FAIL:
                    raise ResponseError(f'Request failed: {code} - {message}.')
                else:
                    raise ResponseError(f'Undefined result status "{result}".')
