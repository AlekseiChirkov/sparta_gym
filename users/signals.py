from django.dispatch import receiver
from django.db.models.signals import post_save

from users.models import MyUser, Profile, Customer


@receiver(post_save, sender=MyUser)
def create_customer_and_user_profile(sender, instance, created, **kwargs):
    print('ok')
    if created:
        Profile.objects.create(user=instance)
        Customer.objects.create(user=instance)

