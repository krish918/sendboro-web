from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from authmod.models import RawUser
from django.db import IntegrityError, transaction
from common.models import User
from common.utils.general import Random, UserTrace
from control.bootstrap import Borouser
from common.models import User, Session
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
try:    
    from django.utils import simplejson
except:
    import simplejson
import re, sys, traceback
from common.base.boroexception import BoroException
from common.base.constant import Const
from common.base.account import Account

class SignonView(View):
    uname = None
    response = {}
    
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(SignonView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.dialcode = request.POST.get('dc',False)
        self.credential = request.POST.get('crdntl',False)
        self.countrycode = request.POST.get('cc',False)
        try:
           res = self.validateInput()
           if isinstance(res, User):
               registeredUser = Borouser(user = res)
               acc = Account(registeredUser)
               self.response = acc.signin(self.uname)
           else:
               unregisterdUser = Borouser(dialcode=self.dialcode,
                                          phone=self.credential,
                                          countrycode=self.countrycode,
                                          req=request)
               acc = Account(unregisterdUser)
               self.response = acc.signup()
                  
        except BoroException as e:
            self.response = {'success' : False, 'errorcode' : e.code }
        except Exception as e:
            self.response = { 'success' : False,
                              'errorcode' : Const.AUTH_ERROR,
                              'message' : e.__str__()
                              }
            
        dump = simplejson.dumps(self.response)
        return HttpResponse(dump, content_type='application/json')
    
    def validateInput(self):
        
        patternUserName = r'^[a-zA-Z][a-zA-Z0-9\.]+$'
        patternAltCredent = r'[a-zA-Z]'
        patternDialCode = r'^\+[0-9]{1,8}$'
        patternPhone = r'[^0-9]'
        
        if self.credential is False or self.dialcode is False or self.countrycode is False:
            raise BoroException("Invalid request.",Const.INVALID_REQUEST)
        
        self.credential = self.credential.strip().replace(' ','')
        self.dialcode = self.dialcode.strip().replace(' ','')
        self.countrycode = self.countrycode.strip()
                
        matchAltCredent = re.search(patternAltCredent, self.credential)
        matchUserName = re.search(patternUserName, self.credential)
        matchDialCode = re.search(patternDialCode, self.dialcode)
        
        if matchAltCredent and matchUserName:
            try:
                user = User.objects.get(username=self.credential)
                self.uname = self.credential
                return user
            except:
                raise BoroException("",Const.USERNAME_NOTEXIST)
            
        elif matchAltCredent and not matchUserName:
            raise BoroException("", Const.INVALID_USERNAME)
        
        elif not matchDialCode or len(self.countrycode) == 0:
            raise BoroException("",Const.INVALID_DIALCODE)
        
        else:
            matchNotPhone = re.search(patternPhone, self.credential)
            fullPhone = self.dialcode + self.credential
            if matchNotPhone or len(self.credential) == 0 or len(fullPhone) > 16:
                raise BoroException("", Const.INVALID_PHONE)
            try:
                user = User.objects.get(phone=self.credential,dialcode=self.dialcode)
                return user
            except:
                pass
            
        return True
            
        
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
            usr = User.objects.get(phone=self.phone,dialcode=self.ac)
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
        