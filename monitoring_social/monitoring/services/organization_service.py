from django.contrib.auth.models import User

from monitoring.models_db.analyzed_items import AnalyzedItemsSummaryStatistics
from monitoring.models_db.organization import Organization


class OrganizationService:

    @staticmethod
    def get_all_organization(user: User):
        return Organization.objects.filter(users=user)
