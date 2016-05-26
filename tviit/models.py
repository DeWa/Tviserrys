from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils.deconstruct import deconstructible
from django.dispatch import receiver
from django.forms import ModelForm
import uuid, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

rename_image = PathAndRename("attachments/screen")
rename_thumbnail = PathAndRename("attachments/thumbs")


class Tviit(models.Model):

    uuid = models.CharField(unique=True, max_length=40, editable=False)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Tviit sender",
    )
    content = models.TextField(max_length=160)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=rename_image, null=True, blank=True)

    thumbnail = models.ImageField(
        upload_to=rename_thumbnail,
        max_length=500,
        null=True,
        blank=True
    )
    reply = models.ForeignKey("self", null=True, blank=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return '%s - %s' % (self.created, self.sender.username)


    def create_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

        # If there is no image associated with this.
        # do not create thumbnail
        if not self.image:
            return

        from PIL import Image
        from cStringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (99, 66)

        DJANGO_TYPE = self.image.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'

        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(StringIO(self.image.read()))

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
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                                 temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        self.thumbnail.save(
            '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf,
            save=False
        )

    def save(self, *args, **kwargs):
        self.create_thumbnail()

        force_update = False

        # If the instance already has been saved, it has an id and we set
        # force_update to True
        if self.id:
            force_update = True

        # Force an UPDATE SQL query if we're editing the image to avoid integrity exception
        super(Tviit, self).save(force_update=force_update)





class TviitForm(ModelForm):

    class Meta:
        model = Tviit
        fields = ['content', 'image']


class EditTviitForm(ModelForm):
    #attachments = MultiFileField(required=False, max_num=12, max_file_size=1024 * 1024 * 500)

    class Meta:
        model = Tviit
        fields = ['content', 'image']