from django.db import models
from ..api.models import *


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_role = models.ForeignKey(Role, on_delete=models.CASCADE)
    review = models.TextField(max_length=256)
