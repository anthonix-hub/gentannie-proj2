from .models import user_referal
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender= User)
def post_save_create_profile(sender, instance, created, *args, **kwargs):
    if created:
        user_referal.objects.create(user=instance)
