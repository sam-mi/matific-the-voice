from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.conf import settings


User = get_user_model()

def update_user(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        pass

post_save.connect(update_user, sender=User)
