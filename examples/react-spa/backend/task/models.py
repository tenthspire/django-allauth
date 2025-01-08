from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    estimate_time = models.PositiveIntegerField()

    def __str__(self):
        return self.name