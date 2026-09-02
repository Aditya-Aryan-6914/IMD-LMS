from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TraineeProfile, TrainerProfile, User


@receiver(post_save, sender=User)
def create_role_profile(sender, instance, created, **kwargs):
    """Ensure every trainee/trainer has their profile row, no matter how
    the user was created (register form, Django admin, shell, etc.)."""
    if not created:
        return
    if instance.role == User.Role.TRAINEE:
        TraineeProfile.objects.get_or_create(user=instance)
    elif instance.role == User.Role.TRAINER:
        TrainerProfile.objects.get_or_create(user=instance)
