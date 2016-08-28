from django.conf.urls import patterns, include, url
from django.contrib import admin
from sendboro import views,settings
from django.views import static

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^team$', views.teamcontainer, name="team"),
    url(r'^partial/team$', views.team),
    url(r'^decorator/feature-panel$', views.featurePanel, name='featurepanel'),
    url(r'^decorator/auth-panel$', views.authPanel, name='authpanel'),
    url(r'^decorator/auth-problem-panel$', views.authProblemPanel, name='authproblempanel'),
    url(r'^partial/init$', views.initView, name="initview"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^authmod/', include('authmod.urls')),
    url(r'^', include('home.urls')),
    url(r'^', include('authmod.urls')),
    url(r'^', include('com.urls')),
    url(r'^api/', include('REST.urls')),
    url(r'^file/', include('file.urls')),
 #   url(r'^content/(?P<path>.*)$', static.serve, 
  #          {'document_root': settings.MEDIA_ROOT}),
]