from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/(?P<userId>[a-zA-Z0-9_@.\-]+/$)', views.userDash, name='userDash'),
    url(r'^allusers/$', views.allUsers, name='allUsers')
]