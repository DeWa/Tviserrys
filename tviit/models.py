from __future__ import unicode_literals
from django.conf import settings
import uuid


from django.db import models

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
    reply = models.ForeignKey("self", null=True, blank=True)


    class Meta:
        ordering = ('created',)