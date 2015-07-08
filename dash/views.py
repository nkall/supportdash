from django.shortcuts import render
from .models import *

import pygal
from pygal.style import *
from datetime import datetime, timedelta

import uuid

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

def allUsers(request):
	ticketsInfo = TicketsInfo(None)
	commentsInfo = CommentsInfo(None)
	surveyInfo = SurveyInfo(None)
	return render(request, 'dash/allusers/index.html', {'ticketsInfo':ticketsInfo,
	              'commentsInfo':commentsInfo, 'surveyInfo':surveyInfo})


'''
  Abstract class for the different objects to be passed to the view: tickets answered, comments
  posted, and survey responses.

  If userId is "None", all users will be queried
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

	# Returns tuples with the uuid in html link, then the count
	def getTopClosers(self):
		agentClosedCount = {}
		for closer in self.objList:
			closerId = closer.actor_id
			closedCount = agentClosedCount.get(closerId, 0) + 1
			agentClosedCount[closerId] = closedCount
		sortedDictKeys = sorted(agentClosedCount, key=agentClosedCount.get)
		userCountTuples = []
		for key in sortedDictKeys[::-1]:
			userCountTuples.append(('<a href="/dash/user/' + str(key) + '">' + str(key) + '</a>', agentClosedCount[key]))
		if len(userCountTuples) > 25:
			userCountTuples = userCountTuples[:25]
		return userCountTuples

	def __init__(self, userId):
		self.userId = userId
		if self.userId:
			allChanges = Event.objects.filter(actor_id=self.userId, type='Change').order_by('-created_at')
		else:
			allChanges = Event.objects.filter(type='Change').order_by('-created_at')
		self.objList = [chg for chg in allChanges if self.changeIsClose(chg.change)]
		self.chart = self.genChart()
		self.count = len(self.objList)
		if not self.userId:
			self.topClosers = self.getTopClosers()

class CommentsInfo(InfoObj):
	def genChart(self):
		ccg = CommentsChart(self.userId, self.objList)
		return ccg.generate()

	def __init__(self, userId):
		self.userId = userId
		if self.userId:
			self.objList = Event.objects.filter(actor_id=self.userId, type='Comment').order_by('-created_at')
		else:
			self.objList = Event.objects.filter(type='Comment').order_by('-created_at')
		self.chart = self.genChart()
		self.count = len(self.objList)

class SurveyInfo(InfoObj):
	def genChart(self):
		scg = SurveyChart(self.userId, self.objList)
		return scg.generate()

	def __init__(self, userId):
		self.userId = userId
		if self.userId:
			self.objList = Survey.objects.filter(actor_id=self.userId).order_by('-created_at')
		else:
			self.objList = Survey.objects.order_by('-created_at')
		self.chart = self.genChart()
		if self.objList:
			self.count = round(100 * (sum([sur.support_score for sur in self.objList]) / len(self.objList)), 1)
		else:
			self.count = 0


class UserDashGenerator:
	def getUserInfo(self):
		print(self.uid)
		uinfo = Event.objects.raw("SELECT id, user_cache \
		                           FROM events \
		                           WHERE user_cache->>'uuid'= %s", [self.uid])
		if len(list(uinfo)) > 0:
			return uinfo[0].user_cache
		else:
			return None

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
		if len(mainLine) > 0:
			oldAvg = mainLine[0]['value']
			for point in mainLine:
				rollingVal = self.calcRollingAvg(point['value'], oldAvg)
				rollingLine.append({'value': rollingVal, 
					                'label': point['label']})
				oldAvg = rollingVal
		return ('Rolling Avg', rollingLine)

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
		return ('Tickets Closed', line)

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
		return ('Comments', line)

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
			label = survey.comments
			line.append({'value': survey.support_score,
			             'label': label})
		return ('Survey Responses', line)

	def __init__(self, userId, surveys):
		self.uid = userId
		self.surveys = surveys

