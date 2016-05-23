from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User



class UserProfile(models.Model):
  user = models.OneToOneField(User)
  description = models.TextField(max_length=3000)
  picture = models.ImageField(blank=True, upload_to='media/profiles/')
  thumbnail = models.ImageField(
    upload_to='media/profiles/thumb/',
    max_length=500,
    null=True,
    blank=True
  )
  follows = models.ManyToManyField("self", blank=True)

# Create UserProfile when user is created
@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
      profile = UserProfile(user=user)
      profile.save()