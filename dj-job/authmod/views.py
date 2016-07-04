from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt 
from authmod.models import RawUser, CodeHash
from django.db import IntegrityError, transaction
from common.models import User
from common.utils.general import Random, UserTrace
from control.bootstrap import Borouser, Rawuser
from common.base.user import User as Usr
from common.models import User, Session
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
try:    
    from django.utils import simplejson
except:
    import simplejson
import re, sys, traceback
from common.base.boroexception import BoroException
from datetime import datetime
from common.base.constant import Const
from common.base.account import Account
from ua_parser import user_agent_parser as uap
from django.contrib.gis.geoip import GeoIP

class SignonView(View):
    
    def __init__(self):
        self.uname = None
        self.response = {}
    
    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(SignonView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        request.session.clear()
        self.dialcode = request.POST.get('dc',False)
        self.credential = request.POST.get('crdntl',False)
        self.countrycode = request.POST.get('cc',False)
        try:
           res = self.validateInput()
           Usr.request = request
           if isinstance(res, User):
               registeredUser = Borouser.CreateWithUser(res)
               acc = Account(registeredUser)
               self.response = acc.AttemptLogin(self.uname)
               request.session['fullphone'] = res.dialcode + str(res.phone)
               self.response['userid'] = res.userid
           else:
               unRegisteredUser = Rawuser.CreateWithPhone(self.dialcode, self.credential)
               unRegisteredUser.Add()
               self.response = {'dialcode':self.dialcode,
                                'phone':self.credential,
                                'success':True,
                                'countrycode': self.countrycode,}
               #self.response['userobj'] = res.get___name__()
                  
        except BoroException as e:
            self.response = {'success' : False, 'errorcode' : e.code }
        except Exception as e:
            self.response = { 'success' : False,
                              'errorcode' : Const.AUTH_ERROR,
                              'tb' : traceback.format_tb(e.__traceback__),
                              'msg':e.__str__(),
                              }
            
        dump = simplejson.dumps(self.response)
        return HttpResponse(dump, content_type='application/json')
    
    def validateInput(self):
        
        patternUserName = r'^[a-zA-Z][a-zA-Z0-9\.]+$'
        patternAltCredent = r'[a-zA-Z]'
        patternDialCode = r'^\+[0-9]{1,8}$'
        patternPhone = r'[^0-9]'
        patternRepeatedNum = r'^([\d])\1+$'
        
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
            matchRepeatedNum = re.search(patternRepeatedNum, self.credential)
            fullPhone = self.dialcode + self.credential
            if (matchNotPhone or len(self.credential) < 4 
                        or matchRepeatedNum or len(fullPhone) > 16):
                raise BoroException("", Const.INVALID_PHONE)
            try:
                user = User.objects.get(phone=self.credential,dialcode=self.dialcode)
                return user
            except:
                pass
            
        return True
    
class ResendCodeView(View):
    
    def __init__(self):
        self.response = {}
    
    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(ResendCodeView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.phone = request.POST.get('ph',False)
        self.dialcode = request.POST.get('dc',False)
        self.uid = request.POST.get('id',False)
        
        try:
            if self.phone is not False and self.dialcode is not False:
                if len(self.phone) == 0 or len(self.dialcode) == 0:
                    raise Exception("Invalid data")
            Usr.request = request
            if self.uid is not False:
                if 'fullphone' in request.session:
                    bu = Borouser(request.session['fullphone'])
                    bu.SendVeriCode()
            else:
                ru = Rawuser.CreateWithPhone(self.dialcode, self.phone)
                ru.SendVeriCode()
            self.response['success'] = True
        except Exception as e:
                self.response = {
                                 'success': False,
                                 'errorcode': Const.AUTH_ERROR,
                                 'message': traceback.format_tb(e.__traceback__),
                                 }
                
        dump = simplejson.dumps(self.response)
        return HttpResponse(dump, content_type='application/json')
            
class AcceptChallenge(View):
    def __init__(self):
        self.response = {}
        
    def get(self, request, *args, **kwargs):
        try:
            chall_resolved = Const.EMPTY_POLL
            curr_time = datetime.now().timestamp()
            while chall_resolved == Const.EMPTY_POLL and (datetime.now().timestamp() - curr_time) < 30:
                chall_resolved = Account.PollChallenge(request.session['hashid'])
            self.response = {'status': chall_resolved,}
        except Exception as e:
            self.response = {'status': Const.POLL_ERROR, 'error': traceback.format_tb(e.__traceback__),}
        dump = simplejson.dumps(self.response)
        return HttpResponse(dump, content_type='application/json')
                 
        
class InitChallenge(View):
    def __init__(self):
        self.response = {}
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(InitChallenge, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:
            if kwargs['code'] is None or 'hashid' not in request.session:
                raise BoroException('No hashid or challenge found.', Const.AUTH_ERROR)
            self.challenge = kwargs['code']
            self.updateChallenge(request.session['hashid'], False)
            self.response['success'] = True
        except Exception as e:
            self.response = {'success': False, 'message':e.__str__(), 'errorcode':Const.AUTH_ERROR,}
        
        dump = simplejson.dumps(self.response)
        return HttpResponse(dump, content_type="application/json")
    
    def get(self, request, *args, **kwargs):
        if kwargs['hashid'] is None or kwargs['code'] is None:
            raise Http404()
        self.challenge = kwargs['code']
        hashid = kwargs['hashid'][:-1]
        try:
            self.updateChallenge(hashid, request)
            self.response['success'] = True
        except CodeHash.DoesNotExist:
            raise Http404()
        except BoroException as e:
            if e.code == Const.INVALID_CODE:
                raise Http404()
            else:
                self.response['expired'] = True
        except Exception as e:
            #self.response['message'] = e.__str__()
            #self.response['success'] = False
            raise e
            
        return render(request, 'decorator/codeacknowledge.html', self.response)
        
        
    def updateChallenge(self,hashid, getrequest):
        if getrequest is not False:
            trace = UserTrace(getrequest)
            ch = CodeHash.objects.get(id=hashid)
            challengehash = Borouser.createhash(self.challenge, (ch.hash.split('$')[1])[2:-1])
        
            if challengehash != ch.hash:
                raise BoroException("INVALID CODE", Const.INVALID_CODE)
            
            if ch.resolve_status is True:
                raise BoroException("CODE RESOLVED", Const.RESOLVED_CODE)
            
            ch.challenge = self.challenge
            ch.responseagent = trace.getUastring() 
            ch.save()
        else:
            CodeHash.objects.filter(id=hashid,resolve_status=False).update(challenge=self.challenge)
            
class Authenticate(View):
    
    def __init__(self):
        self.response = {}
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Authenticate, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        mode = request.POST.get('mode',False)
        try:
            if mode is False:
                raise BoroException("INVALID REQUEST", Const.AUTH_ERROR)
            if mode == 'i':
                self.userid = request.POST.get('uid', False)
                self.authoriseReturn(request)
            elif mode == 'u':
                self.dialcode = request.POST.get('dc', False)
                self.phone = request.POST.get('ph', False)
                self.countrycode = request.POST.get('cc', False)
                self.authoriseRawUser(request)
            self.response['success'] = True
        except Exception as e:
            self.response = {'success':False, 'message':e.__str__(), 'errorcode':Const.AUTH_ERROR}
            
        dump = simplejson.dumps(self.response)
        return HttpResponse(dump, content_type="application/json")
    
    def authoriseReturn(self, req):
        if self.userid is False:
            raise BoroException("INVALID REQUEST", CONST.AUTH_ERROR)
        user = User.objects.get(userid=self.userid)
        Usr.request = req
        bu = Borouser.CreateWithUser(user)
        acc = Account(bu)
        acc.Signin()
        
    def authoriseRawUser(self, req):
        if self.phone is False or self.dialcode is False or self.countrycode is False:
            raise BoroException("INVALID REQUEST", CONST.AUTH_ERROR)
        Usr.request = req
        bu = Borouser.CreateWithFullCredential(self.dialcode, self.phone, self.countrycode)
        acc = Account(bu)
        acc.Create()
        
    