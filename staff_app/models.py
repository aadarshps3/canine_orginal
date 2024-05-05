from django.db import models

from accounts.models import BaseModel, User

# Create your models here.
class Report(BaseModel):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    staff = models.ForeignKey(User,on_delete=models.CASCADE,related_name='staff_report',null=True,blank=True)
    description = models.TextField(null=True,blank=True)