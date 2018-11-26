# tables

user


class Organizer(models.Model):
    user = models.OneToOneField(User)
    college = models.CharField(max_length=30)
    major = models.CharField(max_length=30)

class Attendant(models.Model):
    user = models.OneToOneField(User)
    college = models.CharField(max_length=30)
    major = models.CharField(max_length=30)