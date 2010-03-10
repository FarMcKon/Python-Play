from datetime import *
import unittest
import sys
import re
""" this module is for easily converting a date written in plain text 
into a datetime object.  This is a fast way to get datetime objects from
human readable dates.

Examples:
	"Thursday" or "Thurs" or "thur", etc -> a datetime object for 13:00 on this (or the next following) T	hursday.
	"tomorrow" -> a datetime oject for 13:00 on the next day
	"today"	   -> a datetime object for 13:00 
		     (or after 13:00) a date time object for an hour from the current time until 22:59
		      (after 22:59PM) a warning is thrown, and an object for tomorrow at 13:00 is created

"""

#TRICKY: list for use of .index function
daysOfTheWeek = ['Monday','Tuesday','Wednesday','Thursday','Friday', 'Saturday','Sunday']
g_daysOfTheWeekRegexs = ['Mon([\.\s]|$|day)','Tues?([\.\s]|$|day)','Weds?([\.\s]|$|nesday)',
'Thurs?([\.\s]|$|day)','Fri?([\.\s]|$|day)','Sat?([\.\s]|$|urday)','Sun([\.\s]|$|day)']

DEBUG = False

class TestClass(unittest.TestCase):

	def testDatetimeByDelta(self):
		tmDT = datetime.today() + timedelta(days=1)
		baseDT = datetime(tmDT.year,tmDT.month,tmDT.day,13, 00, tmDT.second)
		testDT = datetimeByDelta()		
		test2DT = datetimeByDelta(1)
		test3DT = datetimeByDelta(daysInTheFuture=1)	
		self.assertEqual(baseDT, testDT,'badly generated datetime object for dateTimeByDelta')
		self.assertEqual(baseDT, test2DT,'badly generated datetime object for dateTimeByDelta')		
		self.assertEqual(baseDT, test3DT,'badly generated datetime object for dateTimeByDelta')
		pass


	def testDatetimeByTextToday(self):
		baseDT = datetime.today()
		testDT = datetimeByFutureDayText('today')
		self.compareDays(baseDT, testDT,'badly generated datetime object for today')
		test2DT = datetimeByFutureDayText('Today')
		self.compareDays(baseDT, test2DT,'badly generated datetime object for Today ')		
	
	def testDatetimeByTextTomorrow(self):
		tmDT = datetime.today() + timedelta(days=1)
		baseDT = datetime(tmDT.year,tmDT.month,tmDT.day,13, 00, tmDT.second)
		testDT = datetimeByFutureDayText('tomorrow')
		self.compareDays(baseDT, testDT,'badly generated datetime object for today')
		test2DT = datetimeByFutureDayText('Tomorrow')
		self.compareDays(baseDT, test2DT,'badly generated datetime object for Today ')		

	def compareDays(self,datetimeBase,datetime2,textError):
		self.assertEquals(datetimeBase.hour,datetime2.hour,textError + " (hours error)")
		self.assertEquals(datetimeBase.year,datetime2.year,textError + " (year error)")
		self.assertEquals(datetimeBase.month,datetime2.month,textError + " (month error)")
		self.assertEquals(datetimeBase.minute,datetime2.minute,textError + " (minute error)")




def datetimeByFutureDayText(textDate):
	""" does processing to turn a text date 'name' into a datetime object for that date. Exact daytime is set by: 
Examples:
	"Thursday" -> a datetime object for 13:00 on this (or the next following) thursday.
	"tomorrow" -> a datetime oject for 13:00 on the next day
	"today"	   -> a datetime object for 13:00 
		     (or after 13:00) a date time object for an hour from the current time until 22:59
		      (after 22:59PM) a warning is thrown, and an object for tomorrow at 13:00 is created
"""


	nowDT = datetime.today()
	newDT = None
	textDate = textDate.lstrip().rstrip().lower()
	if(textDate == 'today'):
		newDT = datetime.today()
	elif(textDate == 'tomorrow'):
		newDT = datetimeByDelta(daysInTheFuture=1)
	else:
		for regex in g_daysOfTheWeekRegexs:
			matcher = re.compile(regex, re.I);
			if(matcher.search(textDate)):
				newDT = datetimeByWeedayName(textDate)
	return newDT

def datetimeByWeedayName(dayName):
	""" Takes a text weekday name, and returns a datetime
	object for 1PM on this or the next day of the week matching that name"""
	nowDT = datetime.today()
	for regex in g_daysOfTheWeekRegexs:
		matcher = re.compile(regex, re.I);
		if(matcher.search(dayName)):
			break; #regex is now the matched regex

	offset = g_daysOfTheWeekRegexs.index(regex)
	if(offset == nowDT.weekday()):
		return datetime.today()
	elif(offset < nowDT.weekday()):
		offset = offset + 7 - nowDT.weekday()
	elif(offset > nowDT.weekday()):
		offset = offset - nowDT.weekday()
	return datetimeByDelta(daysInTheFuture=offset)


def datetimeByDelta(daysInTheFuture=1,hourOfDay=13, miniute=00):
	""" make a datetime for an item due in the future. Assume 13:00 if no time given"""
	tmDT = datetime.today() + timedelta(days=daysInTheFuture)
	newDT = datetime(tmDT.year,tmDT.month,tmDT.day
		,hourOfDay, miniute, tmDT.second)
	return newDT

def main():
	"""command line main.  this allows someone to type a date in the commandline and generate a 
	datetime object from it, and it prints the object out """
	argString = ' '.join(sys.argv[1:])
	e = datetimeByFutureDayText(argString)
	print "date computed is: " + str(e)


if __name__ == '__main__':
	if(DEBUG):
		import unittest
		unittest.main()   
	else:
		main()


