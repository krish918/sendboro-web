from django.db import models
from common.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import IntegrityError

class Contact(models.Model):

    contactid = models.AutoField(null=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_name = models.CharField(null=False, max_length=512)
    add_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "["+self.contact_name+"]"

class NativeContact(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    contact_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        try:
            NativeContact.objects.get(contact__user=self.contact.user,contact_user=self.contact_user)
            raise IntegrityError()
        except ObjectDoesNotExist:
            super(NativeContact, self).save(*args, **kwargs)

class UnregisteredContact(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    contact_phone = models.CharField(null=False, max_length=18)

    def save(self, *args, **kwargs):
        try:
            UnregisteredContact.objects.get(contact__user=self.contact.user, contact_phone=self.contact_phone)
            raise IntegrityError()
        except ObjectDoesNotExist:
            super(UnregisteredContact, self).save(*args, **kwargs)
            