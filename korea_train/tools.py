from .constants import KST  
from datetime import datetime


def get_date() -> str:
    return datetime.now(KST).strftime('%Y%m%d')


def get_time() -> str:
    return datetime.now(KST).strftime('%H%M00')
