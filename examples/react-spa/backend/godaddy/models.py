from django.db import models

# Create your models here.
class DomainPuchase(models.Model):
    domain_name = models.CharField(max_length=255)
    contact_info = models.JSONField()
    purchse_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,default="Success")

    def __str__(self):
        return self.domain_name

