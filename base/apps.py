from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'


    def ready(self):
        import base.signals
        from .models import Pouch
        default_sizes = ['small', 'medium', 'large']
        for size in default_sizes:
            Pouch.objects.get_or_create(size=size, defaults={'quantity': 0})