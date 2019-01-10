from django.db import models


class PerformanceManager(models.Manager):
    """
    Filter performances for views.
    """

    def by_team(self, team):
        pass
