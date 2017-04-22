from contact.models import Contact,NativeContact,UnregisteredContact
from common.models import User
from home.models import Picture
from django.db import transaction
from django.utils.decorators import method_decorator
from common.base.boroexception import BoroException
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class ContactList(object):

    USER_NAME_INVALID = 100

    def __init__(self, userid, cname):
        self.userid = userid
        self.contact_name = cname

    def setPhone(self, dialcode, phone):
        self.contact_dialcode = dialcode
        self.contact_phone = phone

    def setUsername(self, username):
        self.contact_username = username

    @method_decorator(transaction.atomic)
    def create(self):
        #getting the user for which contact will be saved
        self.current_user = User.objects.get(pk=self.userid)

        #now decided whether the contact is native or unregistered

        if self.contact_phone is not False \
            and self.contact_dialcode is not False:
            self.contact_user = self.checkContactRegistered()
            
        elif self.contact_username is not False:
            try:
                self.contact_user = User.objects.get(username=self.contact_username)
            except:
                raise BoroException("Invalid Username", self.USER_NAME_INVALID)
        else:
            raise BoroException()

        self.clist = Contact(contact_name=self.contact_name, user=self.current_user)
        self.clist.save()

        if self.contact_user is not False:
            self.addNativeContact()
        else:
            self.addUnregisterdContact()

        return self.clist
    
    def checkContactRegistered(self):
        try:
            user = User.objects.get(dialcode=self.contact_dialcode,
                        phone=self.contact_phone)
            return user
        except:
            return False
    
    def addNativeContact(self):
        native_contact = NativeContact(contact=self.clist, contact_user=self.contact_user)
        native_contact.save()
        try:
            contact_picture = Picture.objects.get(user=self.contact_user)
            self.contact_picpath = {
                                    'small': contact_picture.small.url,
                                    'med': contact_picture.med.url,
                                }
        except:
            self.set_silhouetteAsContactPicture()

    def addUnregisterdContact(self):
        unreg_contact = UnregisteredContact(contact=self.clist,
                contact_phone=self.contact_dialcode + self.contact_phone)
        unreg_contact.save()
        self.set_silhouetteAsContactPicture()

    def set_silhouetteAsContactPicture(self):
        self.contact_picpath = {
            'small': 'static/resource/picture/silh/silh-80.jpg',
            'med': 'static/resource/picture/silh/silh-150.jpg',
        }