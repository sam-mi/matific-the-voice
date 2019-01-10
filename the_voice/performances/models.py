import uuid

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import IntegerRangeField
from django.contrib.postgres.validators import RangeMinValueValidator, RangeMaxValueValidator
from django.db import models
from django.db.models import QuerySet, DateTimeField, IntegerField
from django_common.models.abstract import AbstractTimeStampedStatusModel, AbstractTimestampedModel
from model_utils import Choices

User = get_user_model()


class Team(AbstractTimeStampedStatusModel):
    """

    """

    title = models.CharField(
        max_length=255,
        help_text="Team name"
    )
    slug = models.CharField(
        max_length=255,
        unique=True,
        default=uuid.uuid4
    )
    mentors = models.ManyToManyField(
        User,
        related_name='teams'
    )
    candidates = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='team',
        blank=True, null=True
    )

    def __str__(self):
        return self.title

    def rank_candidates(self) -> QuerySet:
        """
        Return a list of Performances ordered by the aggregate of scores
        by mentors for the candidates that have completed / created a
        Performance already.

        :return:
        """

    # class Meta:




class Song(AbstractTimestampedModel):
    """
    A Song is Performed by a User
    """

    title = models.CharField(
        max_length=255
    )
    artist = models.CharField(
        max_length=255,
        blank=True, null=True
    )

    def __str__(self):
        return self.title


class Score(AbstractTimestampedModel):
    """
    A score is for a single Performance by a single Mentor

    Scores are aggregated for each performer
    """

    mentor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,

    )
    performance = models.ForeignKey(
        'Performance',
        on_delete=models.CASCADE,
        related_name='scores'
    )
    score = IntegerField(
        # default=NumericRange(0, 101),
        blank=True,
        validators=[
            RangeMinValueValidator(1),
            RangeMaxValueValidator(100)
        ]
    )

    def __str__(self):
        return f'{self.mentor} - {self.performance}'

    class Meta:
        unique_together = ('mentor', 'performance', 'score')


class Performance(AbstractTimeStampedStatusModel):
    """
    A Performance is of a Song, by a Candidate within a Team,
    the performance is scored by each / any mentor in the Team

    Once a Performance is given a slot, it is scheduled and will
    appear
    """

    ACTIVE = AbstractTimeStampedStatusModel.ACTIVE + Choices(
        ('scheduled', 'Performance Scheduled'),
        ('complete', 'Performance Complete'),
    )
    STATUS = Choices(*ACTIVE, *AbstractTimeStampedStatusModel.CLOSED)

    timeslot = DateTimeField(
        db_index=True,
        blank=True, null=True,
        help_text="Performance Time Slot is the date and time that a performance is "
                  "scheduled to take place, including the duration of the performance."
    )
    performer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='performances'
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='performances'
    )

    def get_team(self):
        return self.performer.team

    def is_completed(self):
        if self.score and self.status == self.ACTIVE.complete:
            return True
        return False

    def __str__(self):
        return f'{self.song} by {self.performer}'

    class Meta:
        unique_together = ('performer', 'song')


# class Episode(AbstractTimeStampedStatusModel):
#     """
#     An Episode of the Show
#
#     Each episode is composed of a series of performances with time slots
#     """
