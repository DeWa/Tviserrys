from __future__ import division
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.deconstruct import deconstructible
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.core.validators import RegexValidator
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
  picture = models.ImageField(blank=True, null=True, upload_to=rename_image)
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

  @property
  def get_picture(self):
      if not self.picture:
          return "/static/images/placeholder_user.svg"
      else:
          return self.picture.url

# Resize image and crop it
@receiver(post_save, sender=UserProfile)
def resize_and_crop(sender, **kwargs):
    profile = kwargs["instance"]

    if profile.picture:
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
    else:
        return

class CreateProfileForm(ModelForm):

    username = forms.CharField(label='User name', max_length=20,validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]*$',
            message='Username must contain only numbers and letters',
            code='invalid_username'
        ),
    ])
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    email = forms.EmailField(label='Email', max_length=500)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(CreateProfileForm, self).__init__(*args, **kwargs)

        self.fields['password'].required = False
        self.fields['password2'].required = False

    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2', 'description','picture', 'location']

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'%s already exists' % username)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(u'%s already exists' % email)

    def clean(self, *args, **kwargs):
        cleaned_data = super(CreateProfileForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        # Error if passwords are empty
        if not password or not password2:
            raise forms.ValidationError({'password': ['Password cannot be empty']})
        # Error if passwords aren't the same
        if password != password2:
            raise forms.ValidationError({'password': ['Passwords don\'t match']})

        if len(password) < 6:
            raise forms.ValidationError({'password': ['Minimun length for password is 6 characters']})

        return super(CreateProfileForm, self).clean(*args, **kwargs)



class EditProfileForm(ModelForm):
    first_name = forms.CharField(label='First name', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    last_name = forms.CharField(label='Last name', max_length=100)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'description','picture', 'location']
