from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponseRedirect, HttpResponse
from common.utils.decorator import LoginRequired
from common.utils.general import Random
from django.utils.decorators import method_decorator
from common.models import *
from django.db import transaction
from control.bootstrap import Borouser
try:    
    from django.utils import simplejson
except:
    import simplejson
import traceback, hashlib, uuid

# Create your views here.
class HomeView(View):
    
    @method_decorator(require_GET)
    def dispatch(self, *args, **kwargs):
        return super(HomeView,self).dispatch(*args, **kwargs)
    
    @method_decorator(LoginRequired(url='/'))
    def get(self,request,*args,**kwargs):
        return {
                'url_to_go': request.path,
                }
    
class HomeFrameView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'partial/homeframe.html')

class LogoutView(View):
    
    @method_decorator(require_POST)
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(LogoutView,self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.data = {}
        try:
            Session.objects.filter(pk=int(request.session['session_id'])).update(active=False)
            request.session.clear()
            request.session['logout'] = True
            self.data['success'] = 1
        except:
            self.data['error'] = traceback.format_exc()
            
        data_dump = simplejson.dumps(self.data)
        return HttpResponse(data_dump, content_type='application/json')
    
def ServerError(request):
    response = render(request, '500.html')
    response.status_code = 500
    return response 
    

@LoginRequired()    
def quickContactView(request):
    return render(request, 'partial/quickcontact.html')

@LoginRequired()
def settingsPartialView(request):
    return render(request, 'partial/settings.html')

@LoginRequired()
def sendPartialView(request):
    return render(request, 'partial/send.html')

@LoginRequired()
def sentPartialView(request):
    return render(request, 'partial/sent.html')

@LoginRequired()
def inboxPartialView(request):
    return render(request, 'partial/inbox.html')


@LoginRequired(template='home.html')
def settingsView(request):
    return {}

@LoginRequired(template='home.html')
def sendView(request):
    return {}

@LoginRequired(template='home.html')
def inboxView(request):
    return {}