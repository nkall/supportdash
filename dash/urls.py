from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/(?P<userEmail>[a-zA-Z0-9_@.]+/$)', views.userDash, name='userDash'),
]
