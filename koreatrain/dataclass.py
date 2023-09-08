import logging as log
from dataclasses import dataclass, field
from .tools import get_date, get_time
from .constants import TrainType, PassengerType, Heading, SeatLocation, SeatType, ReserveOption, TRAIN_NAME, NOT_AVAILABLE
from .station import STATION_NAME


@dataclass
class Passenger:
    type_code: PassengerType = PassengerType.ADULT
    count: int = 1

    def __repr__(self) -> str:
        return f'<{self.type_code}, {self.count} 명>'


@dataclass
class Parameter:
    dep: str
    arr: str
    date: str = get_date()
    time: str = get_time()
    time_limit: str = '240000'
    train_type: TrainType = TrainType.ALL
    passengers: list[Passenger] = field(default_factory=lambda: [Passenger()])
    heading: Heading = Heading.DEFAULT
    seat_location: SeatLocation = SeatLocation.DEFAULT
    seat_type: SeatType = SeatType.DEFAULT
    reserve_option: ReserveOption = ReserveOption.GENERAL_FIRST

    def __repr__(self) -> str:
        return f'[{type(self).__name__}] {self.__dict__}'


class Train:
    train_code: str
    train_group: str
    train_name: str
    train_number: str
    dep_date: str
    dep_time: str
    dep_code: str
    dep_name: str
    arr_date: str
    arr_time: str
    arr_code: str
    arr_name: str
    run_date: str
    run_time: str
    delayed: bool
    delay_time: str
    general_seat_state: str
    special_seat_state: str

    def __str__(self) -> str:
        return (
            '[{name} {number}] '
            '{year}년 {month}월 {day}일 '
            '{dep_hour}:{dep_min}~{arr_hour}:{arr_min} / '
            '{dep} -> {arr} / '
            '특실: {special_state}, 일반실: {general_state}'
        ).format(
            name=self.train_name,
            number=self.train_number,
            year=self.dep_date[:4],
            month=self.dep_date[4:6],
            day=self.dep_date[6:],
            dep_hour=self.dep_time[:2],
            dep_min=self.dep_time[2:4],
            arr_hour=self.arr_time[:2],
            arr_min=self.arr_time[2:4],
            dep=self.dep_name,
            arr=self.arr_name,
            special_state=self.special_seat_state,
            general_state=self.general_seat_state,
        )

    def __repr__(self) -> str:
        return str(self)

    def general_seat_available(self):
        return self.general_seat_state not in NOT_AVAILABLE

    def special_seat_available(self):
        return self.special_seat_state not in NOT_AVAILABLE

    def seat_available(self):
        return self.general_seat_available() or self.special_seat_available()


class SRTrain(Train):
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.train_code = data['stlbTrnClsfCd']
        self.train_group = data['trnGpCd']
        self.train_name = TRAIN_NAME[self.train_code]
        self.train_number = data['trnNo']
        self.dep_date = data['dptDt']
        self.dep_time = data['dptTm']
        self.dep_code = data['dptRsStnCd']
        self.dep_name = STATION_NAME[self.dep_code]
        self.arr_date = data['arvDt']
        self.arr_time = data['arvTm']
        self.arr_code = data['arvRsStnCd']
        self.arr_name = STATION_NAME[self.arr_code]
        self.run_date = data['runDt']
        self.run_time = data['runTm']
        self.delayed = data['ocurDlayTnum'] > 0
        self.delay_time = data['ocurDlayTnum']
        self.general_seat_state = data['gnrmRsvPsbStr']
        self.special_seat_state = data['sprmRsvPsbStr']
        log.debug(self)
        log.debug(f'General: {self.general_seat_available()} / Special: {self.special_seat_available()} / Both: {self.seat_available()}')


class KorailTrain(Train):
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.train_code = data['h_trn_clsf_cd']
        self.train_group = data['h_trn_gp_cd']
        self.train_name = data['h_trn_clsf_nm']
        self.train_number = data['h_trn_no']
        self.dep_date = data['h_dpt_dt']
        self.dep_time = data['h_dpt_tm']
        self.dep_code = data['h_dpt_rs_stn_cd']
        self.dep_name = data['h_dpt_rs_stn_nm']
        self.arr_date = data['h_arv_dt']
        self.arr_time = data['h_arv_tm']
        self.arr_code = data['h_arv_rs_stn_cd']
        self.arr_name = data['h_arv_rs_stn_nm']
        self.run_date = data['h_run_dt']
        self.run_time = data['h_run_tm']
        self.delayed = int(data['h_expn_dpt_dlay_tnum']) > 0
        self.delay_time = data['h_expn_dpt_dlay_tnum']
        self.general_seat_state = data['h_spe_rsv_nm']
        self.special_seat_state = data['h_gen_rsv_nm']
        log.debug(self)
        log.debug(f'General: {self.general_seat_available()} / Special: {self.special_seat_available()} / Both: {self.seat_available()}')
