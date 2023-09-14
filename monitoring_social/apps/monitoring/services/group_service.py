from typing import Optional

from apps.monitoring.models_db.search_items import GroupSearchItems


def get_group_by_id(group_id: int) -> Optional[GroupSearchItems]:

    try:
        return GroupSearchItems.objects.get(pk=group_id)
    except GroupSearchItems.DoesNotExist as error:
        raise error
