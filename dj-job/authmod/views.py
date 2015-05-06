from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from authmod.models import RawUser
from django.db import IntegrityError, transaction
from django.db.models import F
from common.models import User
from common.sms import TextMessage
from common.utils.general import Random, UserTrace
from control.bootstrap import Borouser
from common.models import User, Session
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
try:    
    from django.utils import simplejson
except:
    import simplejson
import re, sys, traceback

class SigninView(View):
    
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(SigninView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.phone = request.POST['phone']
        self.ac = request.POST['ac']
        self.code = request.POST['code']
        self.data = {}
        
        try:
            usr = User.objects.get(phone=self.phone,countrycode=self.ac)
            hash = usr.phash
            salt = (hash.split('$')[1])[2:-1]
            givenhash = Borouser().createhash(self.code,salt)
            if hash == givenhash:
                trace = UserTrace(request)
                ip = trace.getIp()
                ua = trace.getUastring()
                
                sess = usr.session_set.create(uastring=ua, ipaddress=ip)
                sid = sess.sessionid
        
                # claro viejo session
                request.session.clear()
        
                #setting session objects
                request.session['user_id'] = usr.userid
                request.session['session_id'] = sid
                
                self.data['success'] = 1
                
            else:
                self.data['error'] = 2
                 
        except ObjectDoesNotExist:
            self.data['error'] = 1
        except:
            self.data['error'] = traceback.format_exc()
            
        dump = simplejson.dumps(self.data)
        return HttpResponse(dump, content_type="application/json")
        
class SignupView(View):
    
    data_dump = {}
    phone = None
    areacode = None
    code = None
    
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(SignupView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.data_dump = {}
        self.code = None
        pattern_ph = r'^\d{10,15}$'
        pattern_ac = r'^\+\d{1,3}$'
        self.phone = request.POST['phone']
        self.areacode = request.POST['ac']
        match_ph = re.search(pattern_ph, self.phone)
        match_ac = re.search(pattern_ac, self.areacode)
 
        if match_ph and match_ac:
            try:
                check_exist = User.objects.get(countrycode=self.areacode, phone=self.phone)
                
                #user already registered
                self.data_dump['error'] = 3
            except:
                #add user as he/she seems fresh
                self.addRawUser(request) 
        else:
            self.data_dump['error'] = 2  #validation error
        
        #prepare json dump for API response
        data = simplejson.dumps(self.data_dump)
        return HttpResponse(data, content_type='application/json')
    
    def addRawUser(self,request):
        try:
            full_phone = self.areacode + self.phone
            self.code = Random(1, 4, 4).create()
            trace = UserTrace(request)
            ip = trace.getIp()
            ua = trace.getUastring()
            ph = RawUser(phone_no=full_phone, vericode=self.code,
                             ipaddress=ip, uastring=ua)
            ph.save()
            self.data_dump['success'] = 1  #fresh user
        except IntegrityError:
             RawUser.objects.filter(phone_no=full_phone).update(vericode=self.code,
                                                                 attempt=F('attempt')+1)
             self.data_dump['success'] = 2  #overwritten request
        except:
             self.data_dump['error'] = 1  # unknown error
        
        if 'success' in self.data_dump:
            self.sendCode(full_phone)
            self.data_dump['phone'] = self.phone
            self.data_dump['areacode'] = self.areacode
            
    
    def sendCode(self, full_phone):
        text = "Your sendboro phone verification code is " + str(self.code) + "."
        sms = TextMessage(text, full_phone)
        sms.send()
        
        
class VerifyCodeView(View):
    code = None
    areacode = None
    phone = None

    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(VerifyCodeView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        datadump = {}
        self.code = request.POST['code']
        self.areacode = request.POST['ac']
        self.phone = request.POST['ph']
        full_phone = self.areacode + self.phone
        
        try:
            get_rawuser = RawUser.objects.get(phone_no=full_phone, vericode=self.code)
            
            #sending request as parameter to initialize session handling
            self.createacc(request)
            
            datadump['success'] = 1
        except ObjectDoesNotExist:
            datadump['error'] = 1
        except MultipleObjectsReturned:
            datadump['error'] = 2
        except:
            datadump['error'] = 3
        
        data = simplejson.dumps(datadump)
        return HttpResponse(data, content_type='application/json')
        
    def createacc(self,request):
        try:
            bu = Borouser(cc=self.areacode, phone=self.phone, req=request)
            bu.create()
        except:
            raise
        