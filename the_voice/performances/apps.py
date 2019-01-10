from django.apps import AppConfig


class PerformancesConfig(AppConfig):
    name = 'the_voice.performances'
    verbose_name = "Performances"

    def ready(self):
        from . import signals

    
