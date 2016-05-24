from __future__ import division
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.deconstruct import deconstructible
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
import uuid, os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from imageresize import imageresize
from tviit.models import Tviit


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

rename_image = PathAndRename("profiles/screen")
rename_thumbnail = PathAndRename("profiles/thumbs")

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  description = models.TextField(max_length=3000, blank=True)
  picture = models.ImageField(blank=True, upload_to=rename_image)
  location = models.CharField(max_length=100, blank=True)
  thumbnail = models.ImageField(
    upload_to=rename_thumbnail,
    null=True,
    blank=True
  )
  follows = models.ManyToManyField("self", blank=True)
  likes = models.ManyToManyField(Tviit, blank=True)

  def __str__(self):
    return '%s userprofile' % (self.user.username)


# Create UserProfile when user is created
@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
      profile = UserProfile(user=user)
      profile.save()

# Resize image and crop it
@receiver(post_save, sender=UserProfile)
def resize_and_crop(sender, **kwargs):
    profile = kwargs["instance"]
    picture = profile.picture
    image = Image.open(picture.path)

    # Get the right ratio
    width, height = image.size
    ratio = width / height

    if width <= height:
        new_width = 200
        new_height = new_width / ratio
    else:
        new_height = 200
        new_width = new_height * ratio


    new_height = int(round(new_height))
    new_width = int(round(new_width))

    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    image = image.crop((0, 0, 200, 200))
    image.save(picture.path)


class EditProfileForm(ModelForm):
    first_name = forms.CharField(label='First name', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    last_name = forms.CharField(label='Last name', max_length=100)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'description','picture', 'location']
