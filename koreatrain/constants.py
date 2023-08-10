from enum import Enum
from datetime import timezone, timedelta


KST = timezone(timedelta(hours=9))


class Platform(Enum):
    SR = 0
    KORAIL = 1
