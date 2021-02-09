from django.dispatch import receiver
from django.db.models.signals import post_save

from users.models import MyUser, Profile, Customer


@receiver(post_save, sender=MyUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=MyUser)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email
        )

