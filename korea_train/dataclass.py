from SRT import Passenger, SeatType
from korail2 import TrainType, Passenger, ReserveOption 
from .tools import get_date, get_time
from dataclasses import dataclass


@dataclass
class Parameter:
    dep: str
    arr: str
    date: str | None = get_date()
    time: str | None = get_time()
    time_limit: str | None = None
    passengers: list[Passenger] | None = None

@dataclass
class SRParameter(Parameter):
    reserve_option: SeatType = SeatType.GENERAL_FIRST
    window: bool | None = None

    def __repr__(self) -> str:
        return f'[{type(self).__name__}] {self.__dict__}'


@dataclass
class KorailParameter(Parameter):
    train_type: TrainType = TrainType.ALL
    reserve_option: ReserveOption = ReserveOption.GENERAL_FIRST

    def __repr__(self) -> str:
        return f'[{type(self).__name__}] {self.__dict__}'
