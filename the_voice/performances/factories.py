
import factory
import random
from factory import lazy_attribute
from faker import Factory
from slugify import slugify
from django.contrib.auth import get_user_model

from the_voice.performances.models import Team, Song, Performance, Score

fake = Factory.create()

User = get_user_model()

class RandomUserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = lazy_attribute(lambda o: fake.email())
    name = lazy_attribute(lambda o: fake.name())


class RandomTeamFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Team

    title = lazy_attribute(lambda o: fake.sentence())
    slug = lazy_attribute(lambda o: slugify(o.title))

    @factory.post_generation
    def mentors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for mentor in extracted:
                self.mentors.add(mentor)


class RandomSongFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Song

    title = lazy_attribute(lambda o: fake.sentence())
    artist = lazy_attribute(lambda o: fake.name())


class PerformanceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Performance

    @factory.post_generation
    def performers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for performer in extracted:
                self.performers.add(performer)

    song = factory.SubFactory(RandomSongFactory)


class RandomScoreFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Score

    score = lazy_attribute(lambda s: random.randrange(0, 100))
