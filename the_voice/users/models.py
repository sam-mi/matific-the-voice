from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices


USER_TYPE_CHOICES = Choices(
    ('admin', 'Administrator'),
    ('mentor', 'Mentor'),
    ('candidate', 'Candidate'),
)

@python_2_unicode_compatible
class User(AbstractUser):

    user_type = models.CharField(
        choices=USER_TYPE_CHOICES,
        max_length=12,
        blank=True, null=True
    )

    # First Name and Last Name do not cover name patterns around the globe.
    salutation = models.CharField(_('Salutation'), blank=True, null=True, max_length=55)
    name = models.CharField(_('Name of User'), blank=True, null=True, max_length=255)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_full_name(self):
        if not self.name == '':
            return self.name
        else:
            return self.username

    @property
    def is_mentor(self):
        return self.user_type == USER_TYPE_CHOICES.mentor

    @property
    def is_candidate(self):
        return self.user_type == USER_TYPE_CHOICES.candidate

    @property
    def is_admin(self):
        if self.is_staff or self.is_superuser:
            return True
        return self.user_type == USER_TYPE_CHOICES.admin

