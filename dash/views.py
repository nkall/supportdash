from django.shortcuts import render
from .models import *
from django.views.generic.list import ListView

import json
from datetime import datetime

# Create your views here.
def index(request):
	return render(request, "dash/index.html")

def userDash(request, userId):
	userId = userId[:-1]
	dashGen = userDashGenerator(userId)
	surveys = dashGen.getSurveyList(0,0)
	userInfo = dashGen.getUserInfo()	
	return render(request, 'dash/user/index.html', {'userId':userId, 'surveys':surveys, 'userInfo':userInfo})

class userDashGenerator():
	def getUserInfo(self):
		uinfo = Event.objects.raw("SELECT id, user_cache \
		                           FROM events \
		                           WHERE user_cache->>'uuid'= %s", [self.uid])[0];
		return uinfo.user_cache

	def getSurveyList(self, lowerBound, upperBound):
		return Survey.objects.filter(actor_id=self.uid).order_by('-created_at')

	def __init__(self, userId):
		self.uid = userId