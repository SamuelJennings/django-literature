from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Literature, Name


@receiver(post_delete, sender=Literature)
def delete_name(sender, instance, **kwargs):
    Name.objects.filter(literature=instance).delete()
