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

path_and_rename = PathAndRename("attachments")


class Tviit(models.Model):

    uuid = models.CharField(unique=True, max_length=40, default=uuid.uuid4().int, editable=False)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Tviit sender",
    )
    content = models.TextField(max_length=160)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    reply = models.ForeignKey("self", null=True, blank=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return '%s - %s' % (self.created, self.sender.username)





class TviitForm(ModelForm):

    class Meta:
        model = Tviit
        fields = ['content', 'image']


class EditTviitForm(ModelForm):
    #attachments = MultiFileField(required=False, max_num=12, max_file_size=1024 * 1024 * 500)

    class Meta:
        model = Tviit
        fields = ['content', 'image']