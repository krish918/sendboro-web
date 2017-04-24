from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden
from common.models import User
from django.utils.decorators import method_decorator
from common.utils.decorator import LoginRequired
from home.models import Picture
from common.models import User
import simplejson, traceback, re
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import transaction, connection
from django.db.utils import IntegrityError
from file.models import Delivery,File,BlindDelivery
from common.utils.general import Helper,Time,UserTrace
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt 
import traceback, os
from django.contrib.gis.geoip2 import GeoIP2
from sendboro.settings import MEDIA_URL
from django.db.models.functions import Concat
from django.db.models import Q, CharField


class MetaUserView(View):
    
    def __init__(self):
        self.data = {}
        self.sent_data = 0
        self.rec_data = 0
    
    
    @method_decorator(LoginRequired())
    def get(self, request, *args, **kwargs):
        
        #if 'HTTP_X_CSRF_HEADER' not in request.META:
         #   return HttpResponseForbidden()
        
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
                                  'small': '/static/resource/picture/silh/silh-80.jpg',
                                  'med': '/static/resource/picture/silh/silh-150.jpg',
                                  'silh': True
                                  }
                
            #getting new files for this user
            try:
                self.checkBlind(usr,fullphone)
                self.fetchFiles(uid)
                self.fetchSentFiles(uid) 
                self.data['file']['sent_data'] = self.sent_data
                self.data['file']['rec_data'] = self.rec_data                                                 
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
        #fetching senderlist
        with connection.cursor() as cursor:
            query = '''
                select 
                        t3.userid as sender_id,
                        count(*) as total_count,
	                    count(case when status = '0' then 1 end) as new_count,
	                    t3.username as sender_name,
	                    concat(t3.dialcode,t3.phone) as sender_phone,
	                    h.small as sender_picture,
	                    max(sent_ts) last_sent
                from 
	                    (file_delivery  t1 
	                    join 
		                (file_file t2 join 
				            (common_user t3 left outer join home_picture h 
                                    on h.user_id=t3.userid and h.active=true)
				            on t2.author_id=t3.userid) on t1.file_id=t2.fileid) 
	                    join common_user as c 
		                    on t1.user_id= c.userid and c.userid = %s
                group by sender_name,sender_phone,sender_id, sender_picture
                order by last_sent desc
            '''
            cursor.execute(query,[uid])
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        
        #newfiles = Delivery.objects.filter(user=uid).order_by('-file__sent_ts')
                
        newcount = Delivery.objects.filter(user=uid,status='0').count()

        self.data['file'] = {
                           'newcount': newcount,
                           'senderlist': [],
                          }
        if len(result) is not 0:
            for res in result:
                identity = res[('sender_name','sender_phone')[res['sender_name'] is None]]
                
                if res['sender_picture'] is None:
                    picture = '/static/resource/picture/silh/silh-80.jpg'
                else:
                    picture = MEDIA_URL+res['sender_picture']


                #getting all files by this sender
                sender_files = Delivery.objects.filter(user=uid,
                            file__author__userid=res['sender_id']).order_by('-file__sent_ts')
        
                files = []
                for sender_file in sender_files:
                    files.append(getFileMeta(sender_file))

                self.data['file']['senderlist'].append({
                    '_id': res['sender_id'],
                    'identity': identity,
                    'pic':      picture,
                    'total':    res['total_count'],
                    'new':      res['new_count'],
                    'time':     Time(str(res['last_sent'])).getDiff(),
                    'files':    files,
                })
    def fetchSentFiles(self, uid):
        self.data['sent'] = []
        
        sent_files = Delivery.objects.filter(~Q(user__userid=uid),
                Q(file__author__userid=uid)).order_by('-file__sent_ts')
        
        blind_sentfiles = BlindDelivery.objects.filter(Q(file__author__userid=uid)).order_by('-file__sent_ts')
        
        all_sent = list(sent_files) + list(blind_sentfiles)
        all_sent_sorted = sorted(all_sent, key=lambda x: x.file.sent_ts, reverse=True)
        
        if len(all_sent_sorted) is not 0:
            for sent_file in all_sent_sorted:
                self.data['sent'].append(getFileMeta(sent_file,True))

def getFileMeta(delivery, sent=False):
        f = delivery.file
                                
        if f.type:
            file_type = Helper().getFormattedType(f.type,f.filename)
        else:
            file_type = 'NA'
                            
        directlink = '/file/direct?id='+str(f.fileid)+'&url='+str(f.path.url)

        file_meta = {
                    'id'   : f.fileid,
                    'name' : f.filename,
                    'size' : f.size,
                    'type' : file_type,
                    'path' : directlink,
                    'time':Time(str(f.sent_ts)).getDiff(),
                    'tooltip': Time(str(f.sent_ts)).getTooltip(),
                    'status': delivery.status,
        }
        if sent is True:
            if isinstance(delivery, BlindDelivery):
                receiver = delivery.phone
            else:
                receiver = delivery.user.username
                if receiver is None:
                    receiver = delivery.user.dialcode \
                        + str(delivery.user.phone)
            file_meta['receiver'] = receiver
            
        return file_meta


            

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
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AlterView, self).dispatch(*args, **kwargs)
    
    @method_decorator(LoginRequired())
    def post(self, request, *args, **kwargs):
        pattern_un = r'^([a-zA-Z]{1,}[\._\-]?[a-zA-Z0-9]{1,}){1,}$'
        pattern_fn = r'^[a-zA-Z]{1,}[ ][a-zA-Z]{1,}([ ][a-zA-Z]{2,}){0,}$'
        self.uid = request.session.get('user_id', False)
            
        if self.uid is False:
            raise Exception()
        
        # using get method to avoid multivaluedict-keyerror and
        # give a default value when a key is not available
        uname = request.POST.get('username', False)
        fname = request.POST.get('fullname', False)
        
        response = {}
        
        try:
            if uname is not False:
                if re.search(pattern_un, uname):
                    user = User.objects.get(pk=self.uid)
                    user.username = uname
                    user.save()
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
        #response['error'] = uname 
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
                user = User.objects.get(username__iexact=recipient)
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
    
    @method_decorator(csrf_protect)
    def get(self, request, *args, **kwargs):
        header = request.META.get("HTTP_X_CSRFTOKEN");
        ip = UserTrace(request).getIp()
        country = {'success': False}
        if ip:
            try:
                geoip = GeoIP2()
                country['data'] = geoip.country("164.100.78.177")
                    
                country['success'] = True
            except Exception as e:
                country['success'] = str(e).encode()
        res = simplejson.dumps(country)
        return HttpResponse(res, content_type='application/json')

class FetchDeliveryReport(View):

    @method_decorator(LoginRequired())
    def get(self, request, *args, **kwargs):
        self.uid = request.session.get('user_id', False)
        if self.uid is False:
            raise Exception()
        response = {}
        try:
            sent = []
            sent_files = Delivery.objects.filter(~Q(user__userid=self.uid),
                Q(file__author__userid=self.uid)).order_by('-file__sent_ts')
        
            if sent_files.exists():
                for sent_file in sent_files:
                    sent.append(getFileMeta(sent_file,True))
            response['status'] = 'ok'
            response['sent'] = sent
        except Exception as e:
            response['status'] = 'failed'
            response['error'] = str(e)

        
        result = simplejson.dumps(response)
        return HttpResponse(result, content_type='application/json')

        