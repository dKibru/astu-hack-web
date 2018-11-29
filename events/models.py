from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=30)
    detail = models.CharField(max_length=255)
    event_datetime = models.DateTimeField()
    featured = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='topics',on_delete=models.CASCADE)
    def __str__(self):
        return self.title + " by " + self.created_by.username


class Interest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

class EventTag(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

