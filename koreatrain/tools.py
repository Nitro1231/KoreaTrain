from .constants import KST
from functools import reduce
from datetime import datetime


def get_date() -> str:
    return datetime.now(KST).strftime('%Y%m%d')


def get_time() -> str:
    return datetime.now(KST).strftime('%H%M00')


def count(passengers: list, passenger_type: ...) -> int:
    return reduce(lambda x, y: x + y.count, list(filter(lambda x: x.type_code == passenger_type, passengers)), 0)
