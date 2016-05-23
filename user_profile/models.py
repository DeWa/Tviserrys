from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.deconstruct import deconstructible
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
import uuid, os


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
  user = models.OneToOneField(User)
  description = models.TextField(max_length=3000)
  picture = models.ImageField(blank=True, upload_to=rename_image)
  location = models.CharField(max_length=100, blank=True)
  thumbnail = models.ImageField(
    upload_to=rename_thumbnail,
    max_length=500,
    null=True,
    blank=True
  )
  follows = models.ManyToManyField("self", blank=True)

  def __str__(self):
    return '%s userprofile' % (self.user.username)


  def create_thumbnail(self):
    # original code for this method came from
    # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

    # If there is no image associated with this.
    # do not create thumbnail
    if not self.picture:
      return

    from PIL import Image
    from cStringIO import StringIO
    from django.core.files.uploadedfile import SimpleUploadedFile
    import os

    # Set our max thumbnail size in a tuple (max width, max height)
    THUMBNAIL_SIZE = (99, 66)

    DJANGO_TYPE = self.picture.file.content_type

    if DJANGO_TYPE == 'image/jpeg':
      PIL_TYPE = 'jpeg'
      FILE_EXTENSION = 'jpg'
    elif DJANGO_TYPE == 'image/png':
      PIL_TYPE = 'png'
      FILE_EXTENSION = 'png'

    # Open original photo which we want to thumbnail using PIL's Image
    image = Image.open(StringIO(self.picture.read()))

    # We use our PIL Image object to create the thumbnail, which already
    # has a thumbnail() convenience method that contrains proportions.
    # Additionally, we use Image.ANTIALIAS to make the image look better.
    # Without antialiasing the image pattern artifacts may result.
    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

    # Save the thumbnail
    temp_handle = StringIO()
    image.save(temp_handle, PIL_TYPE)
    temp_handle.seek(0)

    # Save image to a SimpleUploadedFile which can be saved into
    # ImageField
    suf = SimpleUploadedFile(os.path.split(self.picture.name)[-1],
                             temp_handle.read(), content_type=DJANGO_TYPE)
    # Save SimpleUploadedFile into image field
    self.thumbnail.save(
      '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
      suf,
      save=False
    )

  def save(self, *args, **kwargs):
    force_update = False

    # If the instance already has been saved, it has an id and we set
    # force_update to True
    if self.id:
      orig = UserProfile.objects.get(pk=self.pk)
      if orig.picture != self.picture:
        self.create_thumbnail()
      force_update = True

    # Force an UPDATE SQL query if we're editing the image to avoid integrity exception
    super(UserProfile, self).save(force_update=force_update)

# Create UserProfile when user is created
@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
      profile = UserProfile(user=user)
      profile.save()


class EditProfileForm(ModelForm):
    first_name = forms.CharField(label='First name', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    last_name = forms.CharField(label='Last name', max_length=100)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'description','picture', 'location']
