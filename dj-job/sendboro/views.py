from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from common.utils.decorator import InactiveSessionRequired

@InactiveSessionRequired()
def index(request):
    context = {}
    if 'logout' in request.session and request.session['logout'] == True:
        context['logout'] = True
        request.session.clear()  
    return context

def teamcontainer(request):
    return render(request,'index.html')

def team(request):
    return render(request, 'partial/team.html')

def initView(request):
    return render(request, 'partial/init.html')

def authPanel(request):
    cookie = {}
    cookie.update(csrf(request))
    return render_to_response('decorator/auth-panel.html',cookie)

def authProblemPanel(request):
    return render(request, 'decorator/auth-problem-panel.html')
