from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Pouch

@receiver(post_migrate)
def create_default_pouches(sender, **kwargs):
    from .models import Pouch
    if not Pouch.objects.exists():
        Pouch.objects.bulk_create([
            Pouch(size="Small", quantity=0),
            Pouch(size="Medium", quantity=0),
            Pouch(size="Large", quantity=0),
        ])

