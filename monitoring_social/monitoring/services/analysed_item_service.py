from typing import Optional

from django.contrib.auth.models import User

from monitoring.models_db.analyzed_items import AnalyzedItemsSummaryStatistics, AnalyzedItem, GroupAnalyzedItems, \
    AnalyzedItemKeywords
from monitoring.models_db.organization import Organization
from monitoring.models_db.statistics import Statistics
from vk_api_app.models_db.vk_post import VkPost


class AnalyzedItemService:

    @staticmethod
    def get_keywords_tuple(*, analysed_item):
        return tuple(AnalyzedItemKeywords.objects.filter(owner=analysed_item))

    @staticmethod
    def update(*, statistic: dict, analysed_item) -> None:
        db_posts = list(VkPost.objects.filter(analysed_item=analysed_item))

        analysed_item_statistics = AnalyzedItemsSummaryStatistics.objects.get(pk=analysed_item.id)
        analysed_item_statistics.likes = statistic['likes']
        analysed_item_statistics.comments = statistic['comments']
        analysed_item_statistics.reposts = statistic['reposts']
        analysed_item_statistics.save()

    @staticmethod
    def get_list(*, organization: Organization, name_grop: str) -> tuple[Optional[AnalyzedItem]]:
        group_analyzed_items = GroupAnalyzedItems.objects.get(name=name_grop)
        return tuple(AnalyzedItem.objects
                     .select_related('summary_statistics').order_by('-summary_statistics__score')
                     .filter(organization=organization, group=group_analyzed_items))

    @staticmethod
    def get_all_groups_by_organization(organization: Organization) -> tuple[GroupAnalyzedItems]:
        return tuple(GroupAnalyzedItems.objects.filter(organization=organization))

    @staticmethod
    def get_by_group(*, organization: Organization, group: str):
        return tuple(AnalyzedItem.objects
                     .filter(organization=organization, group__name=group)
                     .order_by('-summary_statistics__score'))

    @staticmethod
    def _sum_children_statistic(*, analyzed_items: tuple[AnalyzedItem]):
        for analyzed_item in analyzed_items:
            if analyzed_item.parent:
                parent_analysed_item = AnalyzedItem.objects.get(pk=analyzed_item.parent.id)
                parent_summary = AnalyzedItemsSummaryStatistics.objects.get(owner=parent_analysed_item)
                children_summary = AnalyzedItemsSummaryStatistics.objects.get(owner=analyzed_item)

                parent_summary.likes = str(int(parent_summary.likes) + int(children_summary.likes))
                parent_summary.comments = str(int(parent_summary.comments) + int(children_summary.comments))
                parent_summary.reposts = str(int(parent_summary.reposts) + int(children_summary.reposts))
                parent_summary.score = str(int(parent_summary.score) + int(children_summary.score))

                parent_summary.save()

    @staticmethod
    def count_summary(organization):
        analyzed_items = tuple(AnalyzedItem.objects.filter(organization=organization))

        for analyzed_item in analyzed_items:
            statistics_list = tuple(Statistics.objects.filter(owner=analyzed_item))

            likes = sum([int(statistics.likes) for statistics in statistics_list])
            comments = sum([int(statistics.comments) for statistics in statistics_list])
            reposts = sum([int(statistics.reposts) for statistics in statistics_list])
            summary_analyzed_item = AnalyzedItemsSummaryStatistics.objects.get(pk=analyzed_item.id)
            summary_analyzed_item.likes = likes
            summary_analyzed_item.comments = comments
            summary_analyzed_item.reposts = reposts
            summary_analyzed_item.score = likes + comments + reposts
            summary_analyzed_item.save()

        AnalyzedItemService._sum_children_statistic(analyzed_items=analyzed_items)
