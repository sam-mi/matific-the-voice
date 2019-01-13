import math
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Avg, QuerySet
from django.test import TestCase

from the_voice.performances.factories import RandomTeamFactory, RandomUserFactory, \
    PerformanceFactory, RandomScoreFactory
from the_voice.performances.models import Performance, Team, Score, Song
from the_voice.users.models import USER_TYPE_CHOICES

User = get_user_model()

class PerformanceTestCase(TestCase):

    def setUp(self):

        num_candidates = 6
        num_teams = 3

        teams = []
        for team_id in range(num_teams):
            teams.append(RandomTeamFactory.create())

        admins = []
        for a in range(2):
            admins.append(RandomUserFactory.create(
                user_type=USER_TYPE_CHOICES.admin
            ))

        mentors = []
        for m in range(3):
            mentors.append(RandomUserFactory.create(
                user_type=USER_TYPE_CHOICES.mentor
            ))

        candidates = []
        for c in range(num_candidates):
            candidates.append(RandomUserFactory.create(
                user_type=USER_TYPE_CHOICES.candidate,
                team=teams[math.floor(c * 0.5)]
            ))

        teams[0].mentors.add(mentors[0], mentors[1])
        teams[1].mentors.add(mentors[0], mentors[2])
        teams[2].mentors.add(mentors[1], mentors[2])

        performances = []
        for p in range(num_candidates):
            performances.append(PerformanceFactory.create(
                performer=candidates[p],
            ))
            performances[p].team = candidates[p].team
            performances[p].save()

        for p in range(num_candidates):
            for s in range(performances[p].team.mentors.count()):
                score = RandomScoreFactory.build()
                score.mentor = performances[p].team.mentors.all()[s]
                score.performance = performances[p]
                score.save()

    def test_team_rank_candidates(self):
        # test ordering by average ranked score
        for team in Team.objects.all():
            candidates = team.rank_candidates()
            self.assertIs(type(candidates), QuerySet)
            test_candidates = team.candidates.filter(
                    user_type=USER_TYPE_CHOICES.candidate,
                    performances__scores__isnull=False
                ).annotate(
                    avg_score=Avg('performances__scores__score')
                ).order_by('avg_score')
            self.assertQuerysetEqual(
                candidates, test_candidates,
                transform=lambda x: x
            )

    def test_team_performance_average(self):
        team = Team.objects.first()
        users = User.objects.filter(team = team).order_by('-date_joined')
        candidates = team.candidates.all().order_by('-date_joined')
        # check the model relationship hasn't changed
        self.assertQuerysetEqual(
            users, candidates,
            transform=lambda x: x
        )
        # check the average aggregate hasn't changed
        average_score = Performance.objects.filter(
            performer__in=team.candidates.all()
        ).aggregate(average_score=Avg('scores__score'))
        self.assertEqual(team.performance_average, average_score['average_score'])

    def test_team_str(self):
        team = Team.objects.all()
        self.assertEqual(team.__str__(), str(team))


    def test_score_mentor_performance_unique_together(self):
        score = Score.objects.first()
        try:
            Score.objects.create(
                mentor=score.mentor,
                performance=score.performance,
                score=55
            )
        except (IntegrityError, ValidationError):
            pass
        else:
            self.fail()

    def test_score_min_0_max_100(self):
        score = Score.objects.first()
        try:
            score.score=101
            score.save()
        except ValidationError as v:
            self.assertEqual(
                v.messages[0], "Ensure this value is less than or equal to 100."
            )
        try:
            score.score=-1
            score.save()
        except ValidationError as v:
            self.assertEqual(
                v.messages[0], "Ensure this value is greater than or equal to 0."
            )

    def test_performance_is_completed(self):
        performance = Performance.objects.first()
        complete = performance.team is not None and performance.performer.team is not None
        if complete:
            complete = performance.scores.count() == performance.team.mentors.count()
        self.assertEqual(complete, performance.is_completed())

        status_complete = performance.status == performance.ACTIVE.complete
        self.assertTrue(status_complete)


    # TODO: complete tests

    # def test_performance_total_score(self):
    #     self.fail()
    #
    # def test_mentor_not_candidate(self):
    #     # a mentor should not be able to be a candidate
    #     self.fail()


    def tearDown(self):
        pass

