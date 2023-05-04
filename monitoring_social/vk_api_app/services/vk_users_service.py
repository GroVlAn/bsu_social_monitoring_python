from dateutil.relativedelta import relativedelta
from django.db.models import Q

from monitoring.models_db.organization import Organization
from vk_api_app.models_db.vk_user import VkUserStatistics, VkUser, VkUserSummaryStatistics


class VkUsersService:

    @staticmethod
    def get_tuple_by_organization(*, organization_id: int) -> tuple[VkUser]:
        return tuple(VkUser.objects.all().filter(organization=organization_id))

    @staticmethod
    def set_activity(*, activity: int) -> VkUserStatistics:
        activity = VkUserStatistics(activity=activity)
        activity.save()

        return activity

    @staticmethod
    def get_all_by_date(organization: Organization, date_from, date_to=None):
        vk_users = tuple(VkUser.objects.filter(organization=organization))
        if date_to is None:
            date_to = date_from + relativedelta(months=1)
        result = []
        for vk_user in vk_users:
            vk_user_statistics = tuple(VkUserStatistics.objects.filter(
                Q(owner=vk_user) &
                Q(date_from__gte=date_from) &
                Q(date_to__lte=date_to)
            ))
            activity = sum((int(statistic.activity) for statistic in vk_user_statistics))
            data = {
                'vk_user': vk_user,
                'activity': activity
            }
            result.append(data)

        return sorted(result, key=lambda r: r['activity'], reverse=True)[:10]

    @staticmethod
    def count_summary(organization: Organization) -> None:
        vk_users = tuple(VkUser.objects.filter(organization=organization))

        for vk_user in vk_users:
            vk_user_statistics = tuple(VkUserStatistics.objects.filter(owner=vk_user))
            if not VkUserSummaryStatistics.objects.filter(owner=vk_user).exists():
                vk_summary_statistic = VkUserSummaryStatistics(owner=vk_user)
                vk_summary_statistic.score = sum([int(vk_user_statistic.activity)
                                                  for vk_user_statistic in vk_user_statistics])

                vk_summary_statistic.save()
            else:
                vk_summary_statistic = VkUserSummaryStatistics.objects.get(owner=vk_user)
                vk_summary_statistic.score = sum([int(vk_user_statistic.activity)
                                                  for vk_user_statistic in vk_user_statistics])

                vk_summary_statistic.save()

    @staticmethod
    def get_list(*, organization):
        print(organization)
        if not VkUser.objects.filter(organization=organization):
            return tuple()
        return tuple(VkUser.objects.filter(organization=organization).
                     select_related('vk_user_summary').order_by('-vk_user_summary__score')[:10])
