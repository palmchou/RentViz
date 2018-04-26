# coding=utf-8
import pytz
from datetime import datetime, timedelta, date

PST_tz = pytz.timezone('US/Pacific')


def get_UTC_now():
    return datetime.utcnow().replace(tzinfo=pytz.utc)


def get_PST_now():
    return get_UTC_now().astimezone(PST_tz)