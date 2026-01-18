from django.db import models
from users.models import CustomUser

class Job(models.Model):
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
