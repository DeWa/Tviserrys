from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
  user = models.OneToOneField(User)
  description = models.TextField(max_length=3000)
  picture = models.ImageField(upload_to='media/profiles/')
  thumbnail = models.ImageField(
    upload_to='media/profiles/thumb/',
    max_length=500,
    null=True,
    blank=True
  )
  follows = models.ManyToManyField("self", blank=True)


