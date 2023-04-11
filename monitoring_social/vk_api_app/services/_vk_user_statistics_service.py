from datetime import datetime

import pytz

from monitoring.models_db.organization import Organization
from vk_api_app.models_db.vk_user import VkUser, VkUserStatistics


class VkUserStatisticsService:
    @staticmethod
    def create(*, statistics: dict, owner: int, organization: Organization) -> None:
        if VkUserStatistics.objects.filter(date_from=statistics['date_from'], owner__id_user=owner):
            return

        aware_datetime_from = statistics['date_from']
        aware_datetime_to = statistics['date_to']
        formatted_datetime_from = aware_datetime_from.strftime('%Y-%m-%d %H:%M:%S.%f%z' )
        formatted_datetime_to = aware_datetime_to.strftime('%Y-%m-%d %H:%M:%S.%f%z')

        if not VkUser.objects.filter(id_user=owner, organization=organization).exists():
            vk_user = VkUser(id_user=owner, organization=organization)
            vk_user.save()
        else:
            vk_user = VkUser.objects.get(id_user=owner, organization=organization)

        vk_user_statistics = VkUserStatistics(
            activity=statistics['activity'],
            date_from=formatted_datetime_from,
            date_to=formatted_datetime_to,
            owner=vk_user
        )

        vk_user_statistics.save()

    @staticmethod
    def check_date(*, date: datetime, owner_statistics: int) -> None:
        return VkUserStatistics.objects.filter(
            date_from__day=date.day,
            date_from__month=date.month,
            date_from__year=date.year,
            owner__id_user=owner_statistics
        ).exists()

    @staticmethod
    def clear_vk_statistics_by_owner(*, date: datetime, owner_statistics: int) -> None:
        VkUserStatistics.objects.filter(
            date_from__day=date.day,
            date_from__month=date.month,
            date_from__year=date.year,
            owner__id_user=owner_statistics
        ).delete()
