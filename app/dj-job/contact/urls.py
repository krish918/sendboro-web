from django.conf.urls import patterns, include, url
from contact.views import GetContact, AddContact

urlpatterns = [
    url(r'getlist', GetContact.as_view()),
    url(r'put', AddContact.as_view()),
]