from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext

# parametrized decorador
# las variables de decorador es no disponsible en vista 
# así este decorador acibir argumento desde vista sólo

class InactiveSessionRequired:
    
    def __call__(self,view):
        def wrapper(request, *args, **kwargs):
            context = view(request, *args, **kwargs)
            if 'user_id' in request.session:
                if 'url_to_go' in request.session:
                    return HttpResponseRedirect(request.session['url_to_go'])
                return render_to_response('home.html', context,
                                          context_instance=RequestContext(request))
            return render_to_response('index.html',context, 
                                      context_instance=RequestContext(request)) 
        return wrapper

class LoginRequired:
    
    def __init__(self, **kwargs):
        self.target = kwargs
    
    def __call__(self,view):
        def wrapper(request, *args, **kwargs):
            context = view(request, *args, **kwargs)
            if 'user_id' not in request.session:
                if 'url' not in self.target or self.target['url'] != '/':
                    request.session['url_to_go'] = request.path
                return render_to_response('login.html', context,
                                          context_instance=RequestContext(request))
            
            if isinstance(context, HttpResponse):
                return context
            
            if 'url' in self.target:
                return HttpResponseRedirect(self.target['url'])
            elif 'template' in self.target:
                return render_to_response(self.target['template'],context,
                                          context_instance=RequestContext(request))
        return wrapper
