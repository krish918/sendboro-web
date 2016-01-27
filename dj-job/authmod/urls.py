from django.conf.urls import url, patterns
from authmod.views import VerifyCodeView, SigninView, SignonView

urlpatterns = patterns('',
        url(r'^verify$', VerifyCodeView.as_view(), name='verify'),
        url(r'^signin$', SigninView.as_view(), name='signin'),
        url(r'^signon$', SignonView.as_view(), name='signon'),
)