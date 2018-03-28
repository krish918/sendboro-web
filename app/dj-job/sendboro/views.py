from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf
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

def featurePanel(request):
    #cookie = {}
    #cookie.update(csrf(request))
    return render(request, 'decorator/feature-panel.html')

def authPanel(request):
    return render(request, 'decorator/auth-panel.html')

def authProblemPanel(request):
    return render(request, 'decorator/auth-problem-panel.html')
    
def caller(request):
    return render(request, 'call.html')
