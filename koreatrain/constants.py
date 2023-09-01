import re
from enum import Enum
from datetime import timezone, timedelta


KST = timezone(timedelta(hours=9))
EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')
PHONE_NUMBER_REGEX = re.compile(r'(\d{3})-(\d{3,4})-(\d{4})')


class Platform(Enum):
    SR      = 0
    KORAIL  = 1


class TrainType(Enum):                      # Korail 전용
    KTX             = '100'                 # KTX
    SAEMAEUL        = '101'                 # 새마을호
    MUGUNGHWA       = '102'                 # 무궁화호
    TONGGUEN        = '103'                 # 통근열차
    NURIRO          = '102'                 # 누리로
    ALL             = '109'                 # 전체
    AIRPORT         = '105'                 # 공항직통
    KTX_SANCHEON    = '100'                 # KTX-산천
    ITX_SAEMAEUL    = '101'                 # ITX-새마을
    ITX_CHEONGCHUN  = '104'                 # ITX-청춘


class PassengerType(Enum):
    ADULT               = 0                 # 어른 - 만 13세 이상
    CHILD               = 1                 # 어린이 - 만 6세 ~ 12세 어린이
    CHILD_UNDER_6       = 2                 # 유아 - 만 6세 미만 유아
    SENIOR              = 3                 # 경로 - 만 65세 이상 경로
    DISABILITY_1_TO_3   = 4                 # 중증 - 장애의 정도가 심한 장애인(구1~3급)
    DISABILITY_4_TO_6   = 5                 # 경증 - 장애의 정도가 심한 장애인(구1~3급)


class Heading(Enum):                        # 좌석 방향
    DEFAULT     = '000'                     # 기본
    FORWARD     = '009'                     # 순방향석
    BACKWARD    = '010'                     # 역방향석


class SeatLocation(Enum):                   # 좌석 위치
    DEFAULT     = '000'                     # 기본
    SINGLE      = '011'                     # 1인석
    WINDOW      = '012'                     # 창측좌석
    AISLE       = '013'                     # 내측좌석


class SeatType(Enum):                       # 좌석 종류
    DEFAULT                 = '015'         # 기본
    CHILD                   = '019'         # 유아동반 / 편한대화
    LAPTOP                  = '031'         # 노트북
    MANUAL_WHEELCHAIR       = '021'         # 수동휠체어석
    ELECTRIC_WHEELCHAIR     = '028'         # 전동휠체어석
    NURSING_ROOM            = 'XXX'         # 수유실 인접
    SECOND_FLOOR            = '018'         # 2층석
    BIKE_RACK               = '032'         # 자전거거치대


class ReserveOption(Enum):
    GENERAL_FIRST   = 'GENERAL_FIRST'       # 일반실 우선
    GENERAL_ONLY    = 'GENERAL_ONLY'        # 일반실
    SPECIAL_FIRST   = 'SPECIAL_FIRST'       # 특실 우선
    SPECIAL_ONLY    = 'SPECIAL_ONLY'        # 특실
