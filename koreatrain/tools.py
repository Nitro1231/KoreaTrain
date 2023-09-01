import json
from .constants import KST
from functools import reduce
from datetime import datetime


def get_date() -> str:
    return datetime.now(KST).strftime('%Y%m%d')


def get_time() -> str:
    return datetime.now(KST).strftime('%H%M00')


def count(passengers: list, passenger_type: ...) -> int:
    return reduce(lambda x, y: x + y.count, list(filter(lambda x: x.type_code == passenger_type, passengers)), 0)


def save_json(data: dict, file_name: str):
    with open(file_name, 'w', encoding='utf8') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
