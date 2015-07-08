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
	surveyInfo = SurveyInfo(userId)

	return render(request, 'dash/user/index.html', {'userId':userId, 'userInfo':userInfo, 'surveyInfo':surveyInfo})

class SurveyInfo:
	def __init__(self, userId):
		self.surveys = Survey.objects.filter(actor_id=userId).order_by('-created_at')
		scg = SurveyChart(userId, self.surveys)
		self.surveyChart = scg.generate()
		self.surveyPercent = round(100 * (sum([sur.support_score for sur in self.surveys]) / len(self.surveys)), 1)


class UserDashGenerator:
	def getUserInfo(self):
		uinfo = Event.objects.raw("SELECT id, user_cache \
		                           FROM events \
		                           WHERE user_cache->>'uuid'= %s", [self.uid])[0];
		return uinfo.user_cache

	def __init__(self, userId):
		self.uid = userId


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
	def genMainLine(self):
		pass

	def genRollingLine(self, mainLine):
		rollingLine = []
		# First point is always the same as the main line
		rollingLine.append(mainLine[0])
		oldAvg = mainLine[0]['value']
		for point in mainLine[1:]:
			rollingVal = self.calcRollingAvg(point['value'], oldAvg)
			rollingLine.append({'value': rollingVal, 
				                'label': point['label']})
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
		return ('Survey Results', line)

	def __init__(self, userId, surveys):
		self.uid = userId
		self.surveys = surveys


