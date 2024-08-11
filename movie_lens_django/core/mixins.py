import datetime

import pytz
from django.conf import settings


class FormatUnixTimeStampMixin:
    @staticmethod
    def format_unix_timestamp(timestamp: str):
        timezone = pytz.timezone(settings.TIME_ZONE)
        timestamp_obj = datetime.datetime.fromtimestamp(timestamp, tz=timezone)
        return timestamp_obj.strftime("%Y-%m-%d %H:%M:%S")
