from django.shortcuts import render
from .models import *
from django.views.generic.list import ListView


# Create your views here.
def index(request):
    return render(request, "dash/index.html")

def userDash(request, userEmail):
	userEmail = userEmail[:-1]
	return render(request, 'dash/user/index.html', {'user_email':userEmail})