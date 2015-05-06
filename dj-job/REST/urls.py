from django.conf.urls import patterns, url
from REST.views import MetaUserView, PhotoView, AlterView, VerifyView

urlpatterns = patterns('',
        url(r'^metauser$', MetaUserView.as_view()),
        url(r'^photo$', PhotoView.as_view()),
        url(r'^alter$', AlterView.as_view()),
        url(r'^verify$', VerifyView.as_view()),
       
)