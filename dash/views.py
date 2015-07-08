from django.shortcuts import render
from .models import *
from django.views.generic.list import ListView

import json
import pygal
from pygal.style import *
from datetime import datetime

# Create your views here.
def index(request):
	return render(request, "dash/index.html")

def userDash(request, userId):
	userId = userId[:-1]
	dashGen = UserDashGenerator(userId)
	userInfo = dashGen.getUserInfo()
	ticketsInfo = TicketsInfo(userId)
	commentsInfo = CommentsInfo(userId)
	surveyInfo = SurveyInfo(userId)

	return render(request, 'dash/user/index.html', {'userId':userId, 'userInfo':userInfo, 
	              'ticketsInfo':ticketsInfo, 'commentsInfo':commentsInfo, 'surveyInfo':surveyInfo})

'''
  Abstract class for the different objects to be passed to the view: tickets answered, comments
  posted, and survey responses
'''
class InfoObj:
	def genChart(self):
		return None

	def __init__(self, userId):
		self.userId = userId
		self.count = 0
		self.objList = []
		self.chart = None

class TicketsInfo(InfoObj):
	# Returns "true" if the change string indicates a ticket closing
	def changeIsClose(self, chg):
		changeType = chg.get('state', False)
		if changeType and changeType[1] == 'closed':
			return True
		return False

	def __init__(self, userId):
		self.userId = userId
		allChanges = Event.objects.filter(actor_id=self.userId, type='Change')
		self.objList = [chg for chg in allChanges if self.changeIsClose(chg.change)]
		self.count = len(self.objList)

class CommentsInfo(InfoObj):
	def __init__(self, userId):
		self.userId = userId
		self.objList = Event.objects.filter(actor_id=self.userId, type='Comment')
		self.count = len(self.objList)

class SurveyInfo(InfoObj):
	def genChart(self):
		scg = SurveyChart(self.userId, self.objList)
		return scg.generate()

	def __init__(self, userId):
		self.userId = userId
		self.objList = Survey.objects.filter(actor_id=self.userId).order_by('-created_at')
		self.chart = self.genChart
		self.count = round(100 * (sum([sur.support_score for sur in self.objList]) / len(self.objList)), 1)


class UserDashGenerator:
	def getUserInfo(self):
		uinfo = Event.objects.raw("SELECT id, user_cache \
		                           FROM events \
		                           WHERE user_cache->>'uuid'= %s", [self.uid])[0];
		return uinfo.user_cache

	def __init__(self, userId):
		self.uid = userId

'''
	Class extended to create each individual chart (tickets, comments & survey satisfaction)
'''
class Chart:
	def generate(self):
		chart = self.genChart()
		mainLine = self.genMainLine()
		rollingLine = self.genRollingLine(mainLine[1])
		chart.add(mainLine[0], mainLine[1])
		chart.add(rollingLine[0], rollingLine[1])
		return chart.render()

	def genChart(self):
		return pygal.Line(style = BlueStyle,
                          show_legend=True,
                          legend_at_bottom=True)

	# Must be extended by child classes
	def genMainLine(self):
		pass

	def genRollingLine(self, mainLine):
		rollingLine = []
		# First point in rolling avg is always the same as the main line
		oldAvg = mainLine[0]['value']
		for point in mainLine:
			rollingVal = self.calcRollingAvg(point['value'], oldAvg)
			rollingLine.append({'value': rollingVal, 
				                'label': point['label']})
			oldAvg = rollingVal
		return ('Rolling Average', rollingLine)

	def calcRollingAvg(self, newVal, oldAvg):
		decayCoefficient = 0.2
		return decayCoefficient * newVal + (1 - decayCoefficient) * oldAvg

	def __init__(self, userId):
		self.uid = userId

class SurveyChart(Chart):
	def genMainLine(self):
		line = []
		for survey in self.surveys[::-1]:
			label = str(survey.ticket_id) + ': ' + survey.comments
			line.append({'value': survey.support_score,
			             'label': label})
		return ('Survey Responses', line)

	def __init__(self, userId, surveys):
		self.uid = userId
		self.surveys = surveys

class CommentsChart(Chart):
	def genMainLine(self):
		pass

	def getUserComments(self):
		pass

