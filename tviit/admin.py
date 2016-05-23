from django.contrib import admin
from .models import Tviit

class TviitAdmin(admin.ModelAdmin):
    readonly_fields=('uuid',)

admin.site.register(Tviit, TviitAdmin)