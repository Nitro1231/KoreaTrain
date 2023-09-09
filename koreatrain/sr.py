# This code is highly inspired by `srt.py` by Gyeongjae Choi.
# https://github.com/ryanking13/SRT/blob/master/SRT/srt.py


import json
import requests
import logging as log
from datetime import datetime, timedelta
from functools import reduce
from .station import search_station, STATION_CODE
from .dataclass import Parameter, Passenger, SRTrain
from .constants import PassengerType, Heading, ReserveOption, EMAIL_REGEX, PHONE_NUMBER_REGEX
from .errors import NotLoggedInError, SoldOutError, NoResultsError, ResponseError
from .tools import count, save_json, _code_logger


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

PASSENGER_MAP = {
    PassengerType.ADULT: '1',
    PassengerType.CHILD: '5',
    PassengerType.SENIOR: '4',
    PassengerType.DISABILITY_1_TO_3: '2',
    PassengerType.DISABILITY_4_TO_6: '3'
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
        log.info(json_data)

        if json_data.get('strResult') == RESULT_FAIL:
            self.logged_in = False
            log.warning(json_data['MSG'])
            return False
        else:
            self.logged_in = True
            return True


    def logout(self) -> bool:
        res = self.session.post(SR_LOGOUT)
        log.info(res.text.strip())
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
            'psgNum': reduce(lambda x, y: x + y.count, parameter.passengers, 0),                    # Total count
            'psgInfoPerPrnb1': count(parameter.passengers, PassengerType.ADULT),                    # 어른 - 만 13세 이상
            'psgInfoPerPrnb5': count(parameter.passengers, PassengerType.CHILD),                    # 어린이 - 만 6세 ~ 12세 어린이
            'psgInfoPerPrnb4': count(parameter.passengers, PassengerType.SENIOR),                   # 경로 - 만 65세 이상 경로
            'psgInfoPerPrnb2': count(parameter.passengers, PassengerType.DISABILITY_1_TO_3),        # 중증 - 장애의 정도가 심한 장애인(구1~3급)
            'psgInfoPerPrnb3': count(parameter.passengers, PassengerType.DISABILITY_4_TO_6),        # 경증 - 장애의 정도가 심하지 않은 장애인(구4~6급)
            'locSeatAttCd1': parameter.seat_location.value,
            'rqSeatAttCd1': parameter.seat_type.value,
            'trnGpCd': '300',
            'dlayTnumAplFlg': 'Y',
            'seatAttCd': '015',
            'isRequest': 'Y'
        }
        trains = list()
        upper_time_limit = int(parameter.time_limit)
        while True:
            log.debug('Requesting train info...')
            log.debug(data)
            res = self.session.post(SR_SEARCH_SCHEDULE, data=data)
            json_data = json.loads(res.text)

            try:
                assert self._result_check(json_data) # assert True
            except NoResultsError: # No more data
                log.debug('=' * 20 + '[SR / End Point - No more data]' + '=' * 20)
                break

            for info in json_data['outDataSets']['dsOutput1']:
                train = SRTrain(info)
                last_dep_time = train.dep_time

                if int(train.dep_time) < upper_time_limit:
                    if available_only and not train.seat_available():
                        continue
                    trains.append(train)
                else:
                    log.debug('=' * 20 + '[SR / End Point - Reach time limit]' + '=' * 20)
                    break

            next_dep_time = datetime.strptime(last_dep_time, '%H%M%S') + timedelta(seconds=1)
            data['dptTm'] = next_dep_time.strftime('%H%M%S')

        log.debug(str(trains).replace(', [', ',\n['))
        return trains


    def reserve(self, parameter: Parameter, train: SRTrain):
        if not self.logged_in:
            raise NotLoggedInError()
        if not isinstance(parameter, Parameter):
            raise TypeError(f'The `parameter` must be a Parameter instance.')
        elif not isinstance(train, SRTrain):
            raise TypeError(f'The `train` must be a SRTrain instance.')
        elif train.train_code != '17':
            raise ValueError(f'The train must be an `SRT` train, but {train.train_name} was given.')
        elif len(parameter.passengers) <= 0:
            raise ValueError('There must be at least one passenger indicated in the parameter.')

        special_seat = (parameter.reserve_option in [ReserveOption.SPECIAL_FIRST, ReserveOption.SPECIAL_ONLY])
        log.debug(f'Reserve option: {parameter.reserve_option} / Special seat: {special_seat}')
        if not train.seat_available():
            raise SoldOutError()
        elif parameter.reserve_option == ReserveOption.SPECIAL_ONLY and not train.special_seat_available():
            raise SoldOutError()
        elif parameter.reserve_option == ReserveOption.GENERAL_ONLY and not train.general_seat_available():
            raise SoldOutError()
        elif parameter.reserve_option == ReserveOption.SPECIAL_FIRST and not train.special_seat_available():
            special_seat = False
        elif parameter.reserve_option == ReserveOption.GENERAL_FIRST and not train.general_seat_available():
            special_seat = True

        data = {
            'reserveType': '11',
            'jobId': '1101', # 개인 에약
            'jrnyCnt': '1',
            'jrnyTpCd': '11',
            'jrnySqno1': '001',
            'stndFlg': 'N',
            'trnGpCd1': '300', # 차종구분, 300 = SRT
            'stlbTrnClsfCd1': train.train_code,
            'dptDt1': train.dep_date,
            'dptTm1': train.dep_time,
            'runDt1': train.dep_date,
            'trnNo1': '%05d' % int(train.train_number),
            'dptRsStnCd1': train.dep_code,
            'dptRsStnCdNm1': train.dep_name,
            'arvRsStnCd1': train.arr_code,
            'arvRsStnCdNm1': train.arr_name,
            'totPrnb': reduce(lambda x, y: x + y.count, parameter.passengers, 0),
            'psgGridcnt': str(len(parameter.passengers))
        }
        for i, passenger in enumerate(parameter.passengers):
            data[f'psgTpCd{i + 1}'] = str(PASSENGER_MAP[passenger.type_code])
            data[f'psgInfoPerPrnb{i + 1}'] = str(passenger.count)
            data[f'locSeatAttCd{i + 1}'] = parameter.seat_location.value
            data[f'rqSeatAttCd{i + 1}'] = parameter.seat_type.value
            data[f'dirSeatAttCd{i + 1}'] = Heading.FORWARD.value # Heading ('009': 정방향)
            data[f'smkSeatAttCd{i + 1}'] = '000'
            data[f'etcSeatAttCd{i + 1}'] = '000'
            data[f'psrmClCd{i + 1}'] = '2' if special_seat else '1' # SeatType: ('1': 일반실, '2': 특실)

        log.info(data)
        res = self.session.post(SR_RESERVE, data=data)
        json_data = json.loads(res.text)
        log.info(json_data)
        self._result_check(json_data)


    def _result_check(self, json_data: dict):
        status = json_data['resultMap'][0]
        result = status.get('strResult')
        code = status['msgCd']
        message = status['msgTxt']
        log.debug('SR result check: ' + str(status))
        _code_logger('sr', result, code, message)

        if self.feedback:
            log.info(message)

        match code:
            case 'IRG000000': # 정상처리되었습니다.
                return True
            case 'WRG000000': # 조회 결과가 없습니다. 
                raise NoResultsError()
            case _:
                if result == RESULT_SUCCESS:
                    return True
                elif result == RESULT_FAIL:
                    raise ResponseError(f'Request failed: {code} - {message}.')
                else:
                    raise ResponseError(f'Undefined result status "{result}".')
