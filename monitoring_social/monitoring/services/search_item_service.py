from typing import Optional
import datetime
from dateutil.relativedelta import relativedelta

from monitoring.models_db.search_items import SearchItemsSummaryStatistics, SearchItem, GroupSearchItems, \
    SearchItemKeywords
from monitoring.models_db.team import Team
from monitoring.models_db.statistics import Statistics
from vk_api_app.models_db.vk_post import VkPost
from django.db.models import Q

class SearchItemService:

    @staticmethod
    def get_keywords_tuple(*, search_item):
        return tuple(SearchItemKeywords.objects.filter(owner=search_item))

    @staticmethod
    def update(*, statistic: dict, search_item) -> None:
        db_posts = list(VkPost.objects.filter(search_item=search_item))

        search_item_statistics = SearchItemsSummaryStatistics.objects.get(pk=search_item.id)
        search_item_statistics.likes = statistic['likes']
        search_item_statistics.comments = statistic['comments']
        search_item_statistics.reposts = statistic['reposts']
        search_item_statistics.save()

    @staticmethod
    def get_list(*, team: Team, name_grop: str) -> tuple[Optional[SearchItem]]:
        group_analyzed_items = GroupSearchItems.objects.get(name=name_grop)
        return tuple(SearchItem.objects
                     .select_related('summary_statistics').order_by('-summary_statistics__score')
                     .filter(team=team, group=group_analyzed_items))

    @staticmethod
    def get_all_groups_by_team(team: Team) -> tuple[GroupSearchItems]:
        return tuple(GroupSearchItems.objects.filter(team=team))

    @staticmethod
    def get_by_group(*, team: Team, group: str):
        return tuple(SearchItem.objects
                     .filter(team=team, group__name=group)
                     .order_by('-summary_statistics__score'))

    @staticmethod
    def _sum_children_statistic(*, analyzed_items: tuple[SearchItem]):
        for analyzed_item in analyzed_items:
            if analyzed_item.parent:
                parent_search_item = SearchItem.objects.get(pk=analyzed_item.parent.id)
                parent_summary = SearchItemsSummaryStatistics.objects.get(owner=parent_search_item)
                children_summary = SearchItemsSummaryStatistics.objects.get(owner=analyzed_item)

                parent_summary.likes = str(int(parent_summary.likes) + int(children_summary.likes))
                parent_summary.comments = str(int(parent_summary.comments) + int(children_summary.comments))
                parent_summary.reposts = str(int(parent_summary.reposts) + int(children_summary.reposts))
                parent_summary.score = str(int(parent_summary.score) + int(children_summary.score))

                parent_summary.save()

    # TODO fix it
    @staticmethod
    def get_all_by_date(team: Team, group_name: str, date_from, date_to=None):
        group_analyzed_items = GroupSearchItems.objects.get(name=group_name)
        if date_to is None:
            date_to = date_from + relativedelta(months=1)
        analyzed_items = tuple(SearchItem.objects.filter(team=team,
                                                           ))
        result = []
        for analyzed_item in analyzed_items:
            statistics = Statistics.objects.filter(
                Q(owner=analyzed_item) &
                Q(date_from__gte=date_from) &
                Q(date_to__lte=date_to)
            )
            likes = sum([int(statistic.likes) for statistic in statistics])
            comments = sum([int(statistic.comments) for statistic in statistics])
            reposts = sum([int(statistic.reposts) for statistic in statistics])
            score = likes + comments + reposts

            data = {
                'analyzed_item': analyzed_item,
                'likes': likes,
                'comments': comments,
                'reposts': reposts,
                'score': score
            }
            result.append(data)
        for item in result:
            print(item['analyzed_item'].parent_id)
            if item['analyzed_item'].parent_id:
                parent_index = next((index
                                     for (index, value) in enumerate(result)
                                     if value['analyzed_item'].id == item['analyzed_item'].parent_id
                                     ), None)
                result[parent_index]['likes'] += item['likes']
                result[parent_index]['comments'] += item['comments']
                result[parent_index]['reposts'] += item['reposts']
                result[parent_index]['score'] += item['score']
        return sorted(result, key=lambda ai: ai['score'], reverse=True)

    @staticmethod
    def count_summary(team):
        analyzed_items = tuple(SearchItem.objects.filter(team=team))

        for analyzed_item in analyzed_items:
            statistics_list = tuple(Statistics.objects.filter(owner=analyzed_item))

            likes = sum([int(statistics.likes) for statistics in statistics_list])
            comments = sum([int(statistics.comments) for statistics in statistics_list])
            reposts = sum([int(statistics.reposts) for statistics in statistics_list])
            summary_analyzed_item = SearchItemsSummaryStatistics.objects.get(pk=analyzed_item.id)
            summary_analyzed_item.likes = likes
            summary_analyzed_item.comments = comments
            summary_analyzed_item.reposts = reposts
            summary_analyzed_item.score = likes + comments + reposts
            summary_analyzed_item.save()

        SearchItemService._sum_children_statistic(analyzed_items=analyzed_items)
