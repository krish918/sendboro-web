from django.conf.urls import url,patterns
from home.views import * 

urlpatterns = [
                url(r'^home$', HomeView.as_view(), name="home"),
                url(r'^partial/homeframe$', HomeFrameView.as_view(), name="homeframe"),
                url(r'^partial/quickcontact$', quickContactView),
                url(r'^logout$', LogoutView.as_view()),
                url(r'^partial/settings$', settingsPartialView),
                url(r'^partial/send$', sendPartialView),
                url(r'^partial/sent$', sentPartialView),
                url(r'^partial/inbox$', inboxPartialView),
                url(r'^settings$', settingsView),
                url(r'^send$', sendView),
                url(r'^inbox$', inboxView),
            ]