import math
from datetime import datetime, timedelta
from typing import Dict, List, Union


class DateTime:
    """
    Class for date management
    """
    @classmethod
    def current_datetime(cls) -> datetime:
        """
        Function that calculate the current date time
        """
        return datetime.utcnow()

    @classmethod
    def expiration_date(
        cls,
        days: int = 0,
        minutes: int = 0,
        hours: int = 0
     ) -> datetime:
        """
        This function create an instance of timedelta with the parameters sended
        
        :param days: days for create timedelta
        :param minutes: minutes for create timedelta
        :param hours: hours for created timedelta
        """
        delta = timedelta(days=days, minutes=minutes, hours=hours)
        return cls.current_datetime() + delta

    @classmethod
    def format_seconds(cls, seconds: float) -> Dict[str, Union[float, int]]:
        """
        Calculate the days, hours and seconds based in seconds
        :param seconds: interval of time in seconds
        """
        days = 0
        hours = 0
        minutes = 0

        if seconds > 60:
            minutes = seconds / 60
            excess, minutes = math.modf(minutes)
            seconds = excess * 60

        if minutes > 60:
            hours = minutes / 60
            excess, hours = math.modf(hours)
            minutes = excess * 60

        if hours > 24:
            days = hours / 24
            excess, days = math.modf(days)
            hours = excess * 24

        return dict(days=days, hours=hours, minutes=minutes, seconds=seconds)

    @classmethod
    def get_delta_days(cls, start: datetime, end: datetime) -> int:
        """
        Calculates the difference in days between a dates

        :param start: initial date. 
        :param end: final date.
        """
        delta = end - start
        return delta.days

    @classmethod
    def create_date_range(cls, start: datetime, end: datetime) -> List[datetime]:
        """
        Creates a date range based in the days difference

        :param start: initial date 
        :param end: final date
        """
        delta = end - start
        return [start + timedelta(days=i) for i in range(0, delta.days)]
