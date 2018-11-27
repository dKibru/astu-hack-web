from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    organizer = models.BooleanField(default=False)
    attendant = models.BooleanField(default=False)
    email = models.CharField(max_length=30, null=True)
    phone_number = models.CharField(max_length=30, null=True)
    def __str__(self):
        return self.user.username
        

