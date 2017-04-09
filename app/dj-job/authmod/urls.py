from django.conf.urls import url, patterns
from authmod.views import SignonView, ResendCodeView, AcceptChallenge, InitChallenge, Authenticate, SetUserForAndroid

urlpatterns = [
        url(r'^signon$', SignonView.as_view(), name='signon'),
        url(r'^resend$', ResendCodeView.as_view()),
        url(r'^challenge$', AcceptChallenge.as_view()),
        url(r'^(?P<hashid>[1-9][0-9]*/)?(?P<code>[0-9]{5,5})$',InitChallenge.as_view()),
        url(r'^authent$', Authenticate.as_view()),
        url(r'^setuser$', SetUserForAndroid.as_view()),
    
    ]