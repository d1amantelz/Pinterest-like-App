from django.contrib import admin

# Register your models here.
from .models import *


class PinsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author', 'collection', 'video', 'image')
    list_display_links = ('author', 'collection')


admin.site.register(Pins)
admin.site.register(Collections)
admin.site.register(Profile)
