from django.shortcuts import render
from .models import *
from django.views.generic.list import ListView

import json
import pygal
from pygal.style import *
from datetime import datetime, timedelta

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
	def __init__(self, userId):
		self.userId = userId
		self.count = 0
		self.objList = []
		self.chart = None

class TicketsInfo(InfoObj):
	def genChart(self):
		tcg = TicketsChart(self.userId, self.objList)
		return tcg.generate()

	# Returns "true" if the change string indicates a ticket closing
	def changeIsClose(self, chg):
		changeType = chg.get('state', False)
		if changeType and changeType[1] == 'closed':
			return True
		return False

	def __init__(self, userId):
		self.userId = userId
		allChanges = Event.objects.filter(actor_id=self.userId, type='Change').order_by('-created_at')
		self.objList = [chg for chg in allChanges if self.changeIsClose(chg.change)]
		self.chart = self.genChart()
		self.count = len(self.objList)

class CommentsInfo(InfoObj):
	def genChart(self):
		ccg = CommentsChart(self.userId, self.objList)
		return ccg.generate()

	def __init__(self, userId):
		self.userId = userId
		self.objList = Event.objects.filter(actor_id=self.userId, type='Comment').order_by('-created_at')
		self.chart = self.genChart()
		self.count = len(self.objList)

class SurveyInfo(InfoObj):
	def genChart(self):
		scg = SurveyChart(self.userId, self.objList)
		return scg.generate()

	def __init__(self, userId):
		self.userId = userId
		self.objList = Survey.objects.filter(actor_id=self.userId).order_by('-created_at')
		self.chart = self.genChart()
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
		chart.x_labels = self.genLabels()
		return chart.render()

	def genChart(self):
		return pygal.Line(style = BlueStyle,
		                  width=350,
		                  height=350,
                          show_legend=True,
                          show_x_guides=True,
                          x_label_rotation=20,
                          legend_at_bottom=True)

	# Must be extended by child classes
	def genMainLine(self):
		pass

	# List of all dates from today to some arbitrary date in the past
	def genDateRange(self):
		self.dateRange = [datetime.date(datetime.today() - timedelta(days=x)) for x in range(0, 75)]

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

	# Must be extended by child classes
	def genLabels(self):
		pass

	def __init__(self, userId):
		self.uid = userId


class TicketsChart(Chart):
	def genMainLine(self):
		self.populateDateCount()
		self.genDateRange()
		line = []
		daterange = self.dateRange
		for date in reversed(daterange):
			ticketCount = self.ticketDateCount.get(date, 0)
			label = str(date) + ": " + str(ticketCount) + " comments"
			line.append({'value': ticketCount,
			             'label': label})
		return ('Comments Posted', line)

	# Populates the self.commentDateCount dict with counts for each date
	def populateDateCount(self):
		for ticket in self.tickets:
			ticketDate = datetime.date(ticket.created_at)
			newCount = self.ticketDateCount.get(ticketDate, 0) + 1
			self.ticketDateCount[ticketDate] = newCount

	# Same method as in CommentsChart -- this would be better structured w/ inheritance
	def genLabels(self):
		dates = self.dateRange
		labels = []
		labels.append(dates[0].strftime("%m/%d/%y"))
		ld = len(dates)
		if ld == 3:
			labels.append(dates[int(ld / 2)].strftime("%m/%d/%y"))
		elif ld > 3:
			hasLabels = False
			for i in range(12, 2, -1):
				if ((ld-1) % i) == 0:
					for j in range(1, i):
						labels.append(dates[int(((ld)*j) / i)].strftime("%m/%d/%y"))
					hasLabels = True
					break
			if hasLabels is False:
				labels.append(dates[int(ld/3)].strftime("%m/%d/%y"))
				labels.append(dates[int(ld*2 / 3)].strftime("%m/%d/%y"))
		if ld > 1:
			labels.append(dates[ld-1].strftime("%m/%d/%y"))
		return labels

	def __init__(self, userId, tickets):
		self.uid = userId
		self.tickets = tickets
		self.ticketDateCount = {}
		self.dateRange = []

class CommentsChart(Chart):
	def genMainLine(self):
		self.populateDateCount()
		self.genDateRange()
		line = []
		daterange = self.dateRange
		for date in reversed(daterange):
			commentCount = self.commentDateCount.get(date, 0)
			label = str(date) + ": " + str(commentCount) + " comments"
			line.append({'value': commentCount,
			             'label': label})
		return ('Comments Posted', line)

	# Populates the self.commentDateCount dict with counts for each date
	def populateDateCount(self):
		for comment in self.comments:
			commentDate = datetime.date(comment.created_at)
			newCount = self.commentDateCount.get(commentDate, 0) + 1
			self.commentDateCount[commentDate] = newCount

	def genLabels(self):
		dates = self.dateRange
		labels = []
		labels.append(dates[0].strftime("%m/%d/%y"))
		ld = len(dates)
		if ld == 3:
			labels.append(dates[int(ld / 2)].strftime("%m/%d/%y"))
		elif ld > 3:
			hasLabels = False
			for i in range(12, 2, -1):
				if ((ld-1) % i) == 0:
					for j in range(1, i):
						labels.append(dates[int(((ld)*j) / i)].strftime("%m/%d/%y"))
					hasLabels = True
					break
			if hasLabels is False:
				labels.append(dates[int(ld/3)].strftime("%m/%d/%y"))
				labels.append(dates[int(ld*2 / 3)].strftime("%m/%d/%y"))
		if ld > 1:
			labels.append(dates[ld-1].strftime("%m/%d/%y"))
		return labels

	def __init__(self, userId, comments):
		self.uid = userId
		self.comments = comments
		self.commentDateCount = {}
		self.dateRange = []

class SurveyChart(Chart):
	def genMainLine(self):
		line = []
		for survey in reversed(self.surveys):
			label = str(survey.ticket_id) + ': ' + survey.comments
			line.append({'value': survey.support_score,
			             'label': label})
		return ('Survey Responses', line)

	def __init__(self, userId, surveys):
		self.uid = userId
		self.surveys = surveys

