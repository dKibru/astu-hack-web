from django.contrib import admin

# Register your models here.
from .models import Profile, FreeTime

admin.site.register(Profile)
admin.site.register(FreeTime)