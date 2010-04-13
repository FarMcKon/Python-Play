from datetime import *
import unittest
import sys
import re

__author__ = "Far McKon"
__maintainer__ = "Far McKon"
__email__ = "FarMcKon@gmail.com"
__copyright__ = "Copyright 2010, Far McKon Bespoke Industries"
__license__ = "GPL"
__version__ = "0.1.1.0"
__code_uuid__ = "afad1c75-e3e3-4a8c-822d-c7ebd13a367f"

__docformat__ = "restructuredtext"
__doc__ =  """ This module is for easily converting a date written in plain text 
into a datetime object.  This is a fast way to get datetime objects from
human readable dates.

Examples:
	"Thursday" or "Thurs" or "thur", etc -> a datetime object for 13:00 
			on this (or the next following) Thursday.
	"tomorrow" -> a datetime.date object for the next day
	"today"	   -> a datetime.date object for today

"""


#TRICKY: list for use of .index function
#code uuid 6609a841-4360-45f6-ad42-ff7587138016
daysOfTheWeek = ['Monday','Tuesday','Wednesday','Thursday','Friday', 'Saturday','Sunday']
_daysOfTheWeekRegexs = ['Mon([\.\s]|$|day)','Tu(es|e)?([\.\s]|$|day)','Weds?([\.\s]|$|nesday)',
'Th(urs|ur)?([\.\s]|$|day)','Fri?([\.\s]|$|day)','Sat?([\.\s]|$|urday)','Sun([\.\s]|$|day)']

#TODO: add hanling of 2010/03/04 style dates, and internationalization thereof

def numberFromDayOFMonth(dayOfMonthText):
	"""Takes a 'day of month number' and  returns the integer 'day of month number of that"""
	match = re.search("\d\d?", dayOfMonthText);
	if(match): 
		return int(match.group());
	return None

def dateByNameAndDayNumber(textDate):
	""" Takes a text date 'Dayname and numberTh' and tries to read it and return a datetime.date for
	the next date in the future that matche that dayname and day of the month numer. 
	Examples:
	"Thursday the 16th: returns the next Thursday that is on at 16th
	"Tu the 12 " returns the next Tuesday that is on a 12th
	"Fri 22" - returns the next Friday that is a 22nd
"""
	nowDT = datetime.today()
	textDate = textDate.lstrip().rstrip()
	dateNumber = numberFromDayOFMonth(textDate.split(" ")[-1])
	dateName = textDate.split(" ")[0];
	weekdayIndex = weekdayNumberByName(dateName)
	
	if(dateNumber == None):
		return None
	
	# -- try to match that day number and day of week number for this month (after today)
	if(nowDT.day <= dateNumber):
		testDatetime = datetime(nowDT.year,nowDT.month, dateNumber)
		if(testDatetime.weekday() == weekdayIndex): #we matched
			return testDatetime.date()

	# -- otherwise try to match that day number and day of week number in the next 8 months (after today)	
	for i in range(1,8):
		testMonth = nowDT.month + i
				
		if (testMonth < 12):
			testDatetime = datetime(nowDT.year,testMonth, dateNumber).date()
			if(testDatetime.weekday() == weekdayIndex): #we matched
				return testDatetime
		else:	
			testDatetime = datetime(nowDT.year+1, (testMonth%12), dateNumber)
			if(testDatetime.weekday() == weekdayIndex): #we matched
				return testDatetime.date()
	# -- no match. Return nothing	 
	return None


def dateByFutureDayName(textDate):
	""" Takesa a text date 'Dayname', tries to read it, and returns  a datetime.date object 
	for that date.Exact daytime is set by:  Parameter 'textDate' - A text stirng of date info. 
	Examples:
	"Thursday" -> a datetime.date object for next closes Thursday (including today)
	"tomorrow" -> a datetime.date oject for the next day
	"today"	   -> a datetime.date object for today
"""
	newDate = None
	textDate = textDate.lstrip().rstrip().lower()
	if(textDate == 'today'):
		newDate = datetime.today().date()
	elif(textDate == 'tomorrow'):
		newDate = dateByDelta(daysInTheFuture=1)
	else:
		for regex in _daysOfTheWeekRegexs:
			matcher = re.compile(regex, re.I);
			if(matcher.match(textDate)):
				newDate = datetimeByWeekdayName(textDate)
	return newDate

def weekdayNumberByName(dayName):
	""" Takes a text dayname, and returns the weekday number (0 to 6) from that name.
		Examples:
		"Thurs" -> 3
		"monday" -> 0
	"""
	for regex in _daysOfTheWeekRegexs:
		matcher = re.compile(regex, re.I);
		if(matcher.match(dayName)):
			return _daysOfTheWeekRegexs.index(regex)
	return None

def datetimeByWeekdayName(dayName):
	""" Takes a text weekday name, and returns a datetime.date
	object for for the closes next day of the week matching that name, including today
	Examples:
		"Thurs" -> a datetime.date object for next closes Thursday (including today)
		"monday" -> a datetime.date object for next closes Monday (including today)
	"""
	nowDT = datetime.today()
	offset = weekdayNumberByName(dayName)

	if(offset == nowDT.weekday()):
		return datetime.today().date()
	elif(offset < nowDT.weekday()):
		offset = offset + 7 - nowDT.weekday()
	elif(offset > nowDT.weekday()):
		offset = offset - nowDT.weekday()
	return dateByDelta(daysInTheFuture=offset)


def dateByDelta(daysInTheFuture=1):
	"""Make a datetime for an item due in the future, based on the number of days from today."""
	tmDT = datetime.today() + timedelta(days=daysInTheFuture)
	newDate = datetime(tmDT.year,tmDT.month,tmDT.day).date()
	return newDate

def getBestDateFromText(text):
		e = None
		e = dateByNameAndDayNumber(text)
		if(e is None):
			e = dateByFutureDayName(text)
		return e
		
def main():
	"""Allows someone to type a date in the commandline and generate a datetime object from it, 
	and it prints the object out """
	
	usageString = """ This is a commandline interface for converting a 
	date as text into a datetime object. """

	if( len(sys.argv) == 1):
	 	print usageString
	else:	 	
		argString = ' '.join(sys.argv[1:])
		
		e = getBestDateFromText(argString);
		
		if (e is None):
			print "no date match for " + argString
		else:
			print "date computed is: " + str(e)


if __name__ == '__main__':
	main()


