from django import template
import datetime
import pytz
from django.conf import settings

register = template.Library()

def cStatus(value):
	if value == "u":
		return "Upcoming"
	elif value == "s":
		return "Completed"
	elif value == "c":
		return "Cancelled"

def cMethod(value):
	if value == "s":
		return "Skype"
	elif value == "ph":
		return "Phone Call"
	elif value == "ft":
		return "FaceTime"
	elif value == "o":
		return "Face to Face"

def cDuration(value):
	if value == "h":
		return "60 Minutes"
	elif value == "hh":
		return "30 Minutes"
	elif value == "qh":
		return "15 Minutes"

def notesDisabled(value):
	if not value == "s":
		return "disabled"
	else:
		return " "

def othersDisabled(value):
        if not value == "u":
                return "disabled"
        else:
                return " "

def currentTime(value):
        serverTZ = pytz.timezone(settings.TIME_ZONE)
	serverToday = serverTZ.localize(datetime.datetime.now())
        timezone = pytz.timezone(value)
        return serverToday.astimezone(timezone).strftime("%a %b %d, %I:%M %p")

def refundPercent(value):
	if value == "no":
		return "Fifty"
	elif value == "yes":
		return "Twenty"

register.filter('cStatus', cStatus)
register.filter('cMethod', cMethod)
register.filter('cDuration', cDuration)
register.filter('currentTime', currentTime)
register.filter('notesDisabled', notesDisabled)
register.filter('othersDisabled', othersDisabled)
register.filter('refundPercent', refundPercent)
