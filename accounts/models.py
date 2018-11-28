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
    def save(self, *args, **kwargs):
    	super().save(*args, **kwargs)  # Call the "real" save() method.
    	for dd in ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]:
    		if  FreeTime.objects.filter(user=self.user, day=dd).count() == 0:
    			FreeTime(user=self.user, day=dd).save()
    	


    # user = models.OneToOneField(User,on_delete=models.CASCADE,)
class FreeTime(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	day = models.CharField(max_length=30)
	allday = models.BooleanField(default=True)
	start = models.IntegerField(null=True)
	startampm = models.CharField(max_length=30, null=True)
	end = models.IntegerField(null=True)
	endampm = models.CharField(max_length=30, null=True)
	def __str__(self):
		return self.user.username + " on " + self.day
        

