from SRT import Passenger, SeatType
from korail2 import TrainType, Passenger, ReserveOption 
from .tools import get_date, get_time
from dataclasses import dataclass


@dataclass
class Search:
    dep: str
    arr: str
    date: str | None = get_date()
    time: str | None = get_time()
    time_limit: str | None = None


@dataclass
class SRSearch(Search):
    passengers: list[Passenger] | None = None
    reserve_option: SeatType = SeatType.GENERAL_FIRST
    window: bool | None = None

    def __repr__(self) -> str:
        return f'[{type(self).__name__}] {self.__dict__}'


@dataclass
class KorailSearch(Search):
    train_type: TrainType = TrainType.ALL
    passengers: list[Passenger] = None
    reserve_option: ReserveOption = None

    def __repr__(self) -> str:
        return f'[{type(self).__name__}] {self.__dict__}'
