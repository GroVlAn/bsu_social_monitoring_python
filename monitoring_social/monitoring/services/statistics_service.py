from datetime import datetime
import pytz

from monitoring.models_db.search_items import SearchItem
from monitoring.models_db.statistics import Statistics


class StatisticsService:

    @staticmethod
    def create(*, statistics: dict, owner: SearchItem) -> None:
        if Statistics.objects.filter(date_from=statistics['date_from'], owner=owner):
            return

        tz = pytz.timezone('Europe/Moscow')
        aware_datetime_from = statistics['date_from']
        aware_datetime_to = statistics['date_to']
        formatted_datetime_from = aware_datetime_from.strftime('%Y-%m-%d %H:%M:%S.%f%z')
        formatted_datetime_to = aware_datetime_to.strftime('%Y-%m-%d %H:%M:%S.%f%z')

        statistics = Statistics(
            likes=statistics['likes'],
            comments=statistics['comments'],
            reposts=statistics['reposts'],
            date_from=formatted_datetime_from,
            date_to=formatted_datetime_to,
            owner=owner
        )

        statistics.save()

    @staticmethod
    def check_date(*, date: datetime, owner: SearchItem) -> bool:
        return Statistics.objects.filter(
            date_from__day=date.day,
            date_from__month=date.month,
            date_from__year=date.year,
            owner=owner).exists()

    @staticmethod
    def clear_statistics_by_owner(*, date: datetime, owner: SearchItem) -> None:
        Statistics.objects.filter(date_from__day=date.day,
                                  date_from__month=date.month,
                                  date_from__year=date.year,
                                  owner=owner).delete()
