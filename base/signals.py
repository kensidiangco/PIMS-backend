from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Pouch

@receiver(post_migrate)
def create_default_pouches(sender, **kwargs):
    if sender.name == 'base':  # replace with your app's name
        default_sizes = ['small', 'medium', 'large']
        for size in default_sizes:
            Pouch.objects.get_or_create(size=size, defaults={'quantity': 0})
