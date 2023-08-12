# This code is highly inspired by `korail2.py` by Taehoon Kim.
# https://github.com/carpedm20/korail2/blob/master/korail2/korail2.py


import json
import requests
from .dataclass import Parameter
from .errors import LoginError
from .constants import EMAIL_REGEX, PHONE_NUMBER_REGEX


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

DEFAULT_USER_AGENT = 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Nexus 4 Build/LMY48T)'


DEVICE = 'AD'


class Korail():
    def __init__(
            self,
            # parameter: Parameter | None = None,
            username: str | None = None,
            password: str | None = None,
            auto_login: bool = True,
            feedback: bool = False
        ) -> None:

        self.session = requests.session()
        self.session.headers.update({'User-Agent': DEFAULT_USER_AGENT})

        # self.parameter = parameter
        self.username = username
        self.password = password
        self.feedback = feedback

        self.logged_in = False

        if (not (username is None and password is None)) and auto_login:
            self.login()


    def _log(self, msg: str) -> None:
        if self.feedback:
            print('[*Korail]', msg)


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
        j = json.loads(res.text)
        self._log(j)

        if j['strResult'] == 'SUCC' and j.get('strMbCrdNo') is not None:
            self.key = j['Key']
            # self.membership_number = j['strMbCrdNo']
            # self.name = j['strCustNm']
            # self.email = j['strEmailAdr']
            self.logged_in = True
            return True
        else:
            self.logged_in = False
            return False
