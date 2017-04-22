from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from common.base.boroexception import BoroException
from contact.control.create_contact import ContactList
from contact.control.get_contact import ContactUtil
from common.base.constant import Const
from django.db import IntegrityError
import simplejson, traceback

class AddContact(View):

    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(AddContact, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        userid = request.session.get('user_id', False)
        res = {}
        try:
            contact_name = request.POST.get('cn', False)
            if userid is False or contact_name is False:
                raise BoroException()
            
            contact_phone = request.POST.get('cp', False)
            contact_dialcode = request.POST.get('cd', False)
            contact_username = request.POST.get('cu', False)
            
            clist_obj = ContactList(userid, contact_name)
            clist_obj.setPhone(contact_dialcode, contact_phone)
            clist_obj.setUsername(contact_username)
                 
            clist = clist_obj.create()

            res['created_contact'] = clist.contact_name
            res['contact_picture'] = clist_obj.contact_picpath
            res[Const.STATUS] = Const.STATUS_OK

        except IntegrityError:
            res[Const.STATUS] = Const.STATUS_FAILED
            res[Const.ALREADY_EXIST] = True
        except BoroException as e:
            res[Const.STATUS] = Const.STATUS_FAILED
            if e.code == ContactList.USER_NAME_INVALID:
                res[Const.INVALID_USERNAME] = True
        except Exception as e:
            res[Const.STATUS] = str(e)

        response = simplejson.dumps(res)
        return HttpResponse(response, content_type='application/json')

class GetContact(View):
    def get(self, request, *args, **kwargs):
        userid = request.session.get('user_id', False)
        res = {}
        try:
            if userid is False:
                raise BoroException()
            contact_list = ContactUtil(userid)
            res['contacts'] = contact_list.returnContacts()
            res['status'] = Const.STATUS_OK
        except Exception as e:
            res['status'] = traceback.format_tb(e.__traceback__)
        
        response = simplejson.dumps(res)
        return HttpResponse(response, content_type='application/json')



