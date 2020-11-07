from datetime import datetime
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils.timezone import now

from shop.models import *
from shop.cron import check_subscription_expired


# @receiver(post_save, sender=Subscription)
# def check_subscription_expired_signal(sender, instance, created, **kwargs):
#     subscription = Subscription.objects.get()
