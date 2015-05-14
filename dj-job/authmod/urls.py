from django.conf.urls import url, patterns
from authmod.views import SignupView, VerifyCodeView, SigninView

urlpatterns = patterns('',
        url(r'^signup$', SignupView.as_view(), name='signup'),
        url(r'^verify$', VerifyCodeView.as_view(), name='verify'),
        url(r'^signin$', SigninView.as_view(), name='signin'),
)