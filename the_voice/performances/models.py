import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import QuerySet, DateTimeField, IntegerField, Avg
from django_common.models.abstract import AbstractTimeStampedStatusModel, AbstractTimestampedModel
from model_utils import Choices

from the_voice.users.models import USER_TYPE_CHOICES

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

    def __str__(self):
        return self.title

    def rank_candidates(self) -> QuerySet:
        """
        Return a list of Performances ordered by the aggregate of scores
        by mentors for the candidates that have completed / created a
        Performance already.

        :return:
        """
        candidates = self.candidates.filter(
            user_type=USER_TYPE_CHOICES.candidate
        ).annotate(avg_score=Avg('performances__scores__score')).order_by('avg_score')
        return candidates

    @property
    def performance_average(self) -> float:
        """
        Return a running average of scores
        :return:
        """
        average = Performance.objects.filter(
            performer__in=self.candidates.all()
        ).aggregate(average_score=Avg('scores__score'))
        return average['average_score']


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
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )

    def __str__(self):
        return self.mentor.get_full_name()

    class Meta:
        unique_together = ('mentor', 'performance')


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
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='performances',
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

    def total_score(self):
        """
        The average score from all of the cores by mentors
        :return:
        """
        total = self.scores.aggregate(total=Avg('score'))
        return total['total']


    def __str__(self):
        return f'{self.song} by {self.performer.get_full_name()}'

    class Meta:
        unique_together = (
            ('performer', 'song', 'team'),
        )
        ordering = ("-timeslot",)


# TODO: Phase 2 - group performances per episode

# class Episode(AbstractTimeStampedStatusModel):
#     """
#     An Episode of the Show
#
#     Each episode is composed of a series of performances with time slots
#     which are conceptually grouped together as 'actions'
#     """
