from dataclasses import dataclass, field
from .tools import get_date, get_time
from .constants import TrainType, PassengerType, Heading, SeatLocation, SeatType, ReserveOption


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
