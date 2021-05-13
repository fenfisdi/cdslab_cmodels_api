from datetime import datetime, timedelta


class DateTime:

    @classmethod
    def current_datetime(cls) -> datetime:
        return datetime.utcnow()

    @classmethod
    def expiration_date(
        cls,
        days: int = 0,
        minutes: int = 0,
        hours: int = 0
    ) -> datetime:
        delta = timedelta(days=days, minutes=minutes, hours=hours)
        return cls.current_datetime() + delta
