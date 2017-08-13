from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.main, name="main"),
    url(r'^comment/$', views.text_comment, name="text_comment"),
    url(r'^chat_comment/$', views.chat_comment, name="chat_comment"),
    url(r'^location_list/$', views.location_list, name="location_list"),
    url(r'^chat/$', views.chat, name="chat"),
    url(r'^flush/$', views.flush, name="flush"),
]
