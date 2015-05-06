from django.db import models
from django.core.validators import RegexValidator

class RawUser(models.Model):
    phone_no = models.CharField(max_length=16, unique=True)
    vericode = models.CharField(max_length=4, null=False, blank=False)
    attempt = models.IntegerField(default=1)
    uastring = models.CharField(max_length=512, default=None, null=True)
    ipaddress = models.CharField(max_length=16, default=None, null=True)
    ts = models.DateTimeField(auto_now=True, default=None, null=True)
    
    def __str__(self):
        return self.phone_no
