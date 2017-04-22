from contact.models import Contact, NativeContact, UnregisteredContact
from home.models import Picture
from common.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class ContactUtil(object):
    def __init__(self, userid):
        self.user = User.objects.get(pk=userid)

    def returnContacts(self):
        contacts = []
        clist = Contact.objects.filter(user=self.user).order_by('contact_name')

        if clist.exists():
            for cntct in clist:
                cntct_info = {'contact_name':cntct.contact_name,}
                native_contact = contact_phone = False
                try:
                    native_contact = NativeContact.objects.get(contact=cntct)
                    if native_contact.contact_user.username is not None:
                        cntct_info['username'] = native_contact.contact_user.username
                    else:
                        cntct_info['phone'] = native_contact.contact_user.dialcode \
                                + native_contact.contact_user.phone
                    cntct_info['native'] = 1
                except ObjectDoesNotExist:
                    contact_phone = UnregisteredContact.objects.get(contact=cntct)
                    cntct_info['phone'] = contact_phone.contact_phone
                    cntct_info['native'] = 0
                    
                try:
                    if native_contact is not False:
                        contact_pic = Picture.objects.get(user=native_contact.contact_user)
                        cntct_info['picture'] = contact_pic.small.url
                    else:
                        raise NameError()
                except (ObjectDoesNotExist, NameError) as e:
                    cntct_info['picture'] = 'static/resource/picture/silh/silh-80.jpg'

                contacts.append(cntct_info)

        return contacts