from django.conf.urls import url,patterns
from com.views import AutoReplyInXml, CodeSpeechInXml, VoiceCallCode, RecordActionView, RawCallView

urlpatterns = [
               url(r'^com/api/reply$', AutoReplyInXml.as_view()),
               url(r'^com/api/voice/code/(?P<code>[0-9]{5,5})$', CodeSpeechInXml.as_view()),
               url(r'^com/api/voicecall$', VoiceCallCode.as_view()),
               url(r'^com/api/record$', RecordActionView.as_view()),
               url(r'^com/api/rawcall$', RawCallView.as_view()),
            ]