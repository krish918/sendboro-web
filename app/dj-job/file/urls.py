from django.conf.urls import patterns, url
from file.views import PushView, DownloadView, ChangeStateView, DirectLinkView

urlpatterns = [
        url(r'^push$', PushView.as_view()),
        url(r'^download$', DownloadView.as_view()),
        url(r'changestate$',ChangeStateView.as_view()),
        url(r'direct$',DirectLinkView.as_view()),
]