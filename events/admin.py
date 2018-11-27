from django.contrib import admin

# Register your models here.
from .models import Category, Event, Interest, EventTag

admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Interest)
admin.site.register(EventTag)