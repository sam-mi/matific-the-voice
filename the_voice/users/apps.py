from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'the_voice.users'
    verbose_name = "Users"

    def ready(self):
        from . import signals

    
