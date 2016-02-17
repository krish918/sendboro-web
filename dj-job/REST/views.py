from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden
from common.models import User
from django.utils.decorators import method_decorator
from common.utils.decorator import LoginRequired
from home.models import Picture
from common.models import User
import simplejson, traceback, re
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import transaction
from django.db.utils import IntegrityError
from file.models import Delivery,File,BlindDelivery
from common.utils.general import Helper,Time,UserTrace
from django.contrib.gis.geoip import GeoIP


class MetaUserView(View):
    
    def __init__(self):
        self.data = {}
    
    
    @method_decorator(LoginRequired())
    def get(self, request, *args, **kwargs):
        
        if 'HTTP_X_CSRF_HEADER' not in request.META:
            return HttpResponseForbidden()
        
        #getting general user data 
        try:
            uid = request.session['user_id']
            usr = User.objects.get(pk=uid)
            fullphone = str(usr.dialcode)+str(usr.phone)
        
            for key in User._meta.get_all_field_names():
                if key != 'phash':
                    try:
                        val = getattr(usr, key)
                        if val is None:
                            self.data[key] = 0
                        else:
                            self.data[key] = str(val)
                    except:
                        pass
                    
            #getting display pic
            try:
                pic = Picture.objects.get(user=uid, active=True)
                self.data['photo'] = {
                                       'small': pic.small.url,
                                       'med': pic.med.url,
                                       'silh': False
                                       }
            except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
                self.data['photo'] = {
                                  'small': 'static/resource/picture/silh/silh-80.jpg',
                                  'med': 'static/resource/picture/silh/silh-150.jpg',
                                  'silh': True
                                  }
                
            #getting new files for this user
            try:
                self.checkBlind(usr,fullphone)
                self.fetchFiles(uid)
                                                  
            except:
                raise
        except:
            self.data['error'] = traceback.format_exc()

        dump = simplejson.dumps(self.data)
        return HttpResponse(dump, content_type='application/json')
    
    def checkBlind(self,usr,fullphone):
        
        blindfiles = BlindDelivery.objects.filter(phone=fullphone,status='0').order_by('-file__sent_ts')
        if blindfiles.exists():
            for bfile in blindfiles:
                Delivery.objects.create(file=bfile.file,user=usr)
            
            blindfiles.update(status='1')
            
    def fetchFiles(self,uid):
        newfiles = Delivery.objects.filter(user=uid).order_by('-file__sent_ts')
                
        newcount = Delivery.objects.filter(user=uid,status='0').count()
        self.data['file'] = {
                           'newcount': newcount,
                           'lists': []
                          }
        if newfiles.exists():
            for newfile in newfiles:
                file = newfile.file
                        
                sender = file.author
                sender_un = False
                if sender.username is not None:
                    sender_un = sender.username
                sender_phone = str(sender.dialcode)+str(sender.phone)
                        
                if file.type:
                    file_type = Helper().getFormattedType(file.type,file.filename)
                else:
                    file_type = 'NA'
                    
                directlink = 'file/direct?id='+str(file.fileid)+'&url='+str(file.path.url)
                        
                self.data['file']['lists'].append({
                            'id'   : file.fileid,
                            'name' : file.filename,
                            'size' : file.size,
                            'type' : file_type,
                            'path' : directlink,
                            'sender_phone': sender_phone,
                            'sender_un': sender_un,
                            'time':Time(str(file.sent_ts)).getDiff(),
                            'tooltip': Time(str(file.sent_ts)).getTooltip(),
                            'status': newfile.status
                    })

class PhotoView(View):
    
    def __init__(self):
        self.f = None
        self.uid = None
        self.data = None

    @method_decorator(transaction.atomic)
    @method_decorator(LoginRequired())    
    def post(self,request,*args, **kwargs):
        
        try:
            
            self.f = request.FILES['file']
            self.uid = request.session['user_id']
            self.data = {}
        
            if self.f.size > 7000000:
                self.data['error'] = 1;
            elif re.search('image/',self.f.content_type) is None:
                self.data['error'] = 2;
            else:
                self.save_photo(request)
                
        except:
            self.data['error'] = traceback.format_exc()
            
        dump = simplejson.dumps(self.data)
        return HttpResponse(dump, content_type='application/json')
        
    
    def save_photo(self, request):
        
        Picture.objects.filter(user=self.uid).update(active=False)
        usr = User.objects.get(pk=self.uid)
        pic = usr.picture_set.create(large=self.f,med=self.f, small=self.f)
                
        self.data['med'] = pic.med.url
        self.data['small'] = pic.small.url
        
        self.data['success'] = 1
        
class AlterView(View):
    
    @method_decorator(LoginRequired()) 
    def post(self, request, *args, **kwargs):
        pattern_un = r'^([a-zA-Z]{1,}[\._\-]?[a-zA-Z0-9]{1,}){1,}$'
        pattern_fn = r'^[a-zA-Z]{1,}[ ][a-zA-Z]{1,}([ ][a-zA-Z]{2,}){0,}$'
        self.uid = request.session['user_id']
        
        # using get method to avoid multivaluedict-keyerror and
        # give a default value when a key is not available
        uname = request.POST.get('username', False)
        fname = request.POST.get('fullname', False)
        
        response = {}
        
        try:
            if uname is not False:
                if re.search(pattern_un, uname):
                    User.objects.filter(pk=self.uid).update(username=uname)
                    response['uname'] = uname
                    response['success'] = 1
                else:
                    response['error'] = 1
            elif fname is not False:
                if re.search(pattern_fn, fname):
                    User.objects.filter(pk=self.uid).update(fullname=fname)
                    response['fname'] = fname
                    response['success'] = 1
                else:
                    response['error'] = 2
        except IntegrityError:
            response['error'] = 3
        except:
            response['error'] = traceback.format_exc()
        response['error'] = uname 
        res = simplejson.dumps(response)
        return HttpResponse(res, content_type='application/json')
    
class VerifyView(View):
    
    @method_decorator(LoginRequired())
    def post(self, request, *args,**kwargs):
        self.res = {}
        recipient = request.POST['rcpnt']
        reUn = r'^([a-zA-Z]{1,}[\._\-]?[a-zA-Z0-9]{1,}){1,}$'
        rePhone = r'^\+[1-9][0-9]{6,14}$'
        if re.search(reUn, recipient):
            try:
                user = User.objects.get(username=recipient)
                self.res['uid'] = user.userid
                self.res['success'] = 1
            except ObjectDoesNotExist:
                self.res['nouser'] = True
            except:
                self.res['error'] = 1
                
        elif re.search(rePhone, recipient):
            try:
                user = User.objects.raw('''SELECT userid FROM (SELECT userid,
                                 COALESCE(dialcode,'')||COALESCE(phone,0)
                                 AS fullphone FROM common_user) t1  WHERE
                                 fullphone = %s''', [recipient])
                if len(list(user)) is 0:
                    self.res['blind'] = True
                    self.res['phone'] = recipient
                else:
                    self.res['uid'] = user[0].userid
                    self.res['success'] = 1
            except:
                self.res['error'] = traceback.format_exc()
        else:
            self.res['error'] = 3
                
        data = simplejson.dumps(self.res)
        return HttpResponse(data, content_type='application/json')
    
class Country(View):
    
    def get(self, request, *args, **kwargs):
        ip = UserTrace(request).getIp()
        country = {'success': False}
        if ip:
            try:
                geoip = GeoIP()
                country['data'] = geoip.country("airtel.in")
                country['success'] = True
            except TypeError:
                pass
        res = simplejson.dumps(country)
        return HttpResponse(res, content_type='application/json')

        