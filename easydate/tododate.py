import easydate
from datetime import *
import unittest
#import sys
import re

""" This module is for easily converting a text date into a datetime object.

Examples:
	"Thursday" or "Thurs" or "thur", etc -> a datetime object for 13:00 on this (or the next following) Thursday.
	"tomorrow" -> a datetime oject for 13:00 on the next day
	"today"	   -> a datetime object for 13:00 
		     (or after 13:00) a date time object for an hour from the current time until 22:59
		      (after 22:59PM) a warning is thrown, and an object for tomorrow at 13:00 is created
	"Wed at 3PM" -> a datetime object for this or the next wedsnesday at 1500
	"Last Wed at 3PM" -> a datetime object for the previous wedsnesday at 1500
	"Wed the 15th at 3PM" -> a datetime object for the first '15th' in the next 3 months that is a wednesday
"""


g_daysOfTheWeekRegexs = ['Mon([\.\s]|$|day)','Tues?([\.\s]|$|day)','Weds?([\.\s]|$|nesday)',
'Thurs?([\.\s]|$|day)','Fri?([\.\s]|$|day)','Sat?([\.\s]|$|urday)','Sun([\.\s]|$|day)']
g_breakerRegexes = [" at "]

# 1) is it of the format 1AM - 12PM style (w/o minutes)
g_dateRegex = '(([01]?[0-9])((A|P)\.?M\.?))'
## 2) is it of the format 00:00 24:59 style
g_dateRegex2 = '(([0-1][0-9])|(2[0-3])):?([0-5][0-9])' #index 0 is hour, index 3 is min


DEBUG = True

class TestClass(unittest.TestCase):
	def testDatetimeByDelta(self):
		time = timebyText("12AM")
		self.assertEqual(str(time),'12:00:00',"Fail for 12:00:00 vs " + str(time))
		time = timebyText("2300")
		self.assertEqual(str(time),'23:00:00',"Fail for 23:00:00 vs " + str(time))
		time = timebyText("2210")
		self.assertEqual(str(time),'22:10:00',"Fail for 22:10:00 vs " + str(time))
		time = timebyText("2500")
		self.assertEqual(str(time),'None',"erronous success for 2500 vs " + str(time))
		print time
		#self.assertEqual(0,1,"test fail")
	

def timebyText(text):
	matchedTime = None
	time1Reg = re.compile(g_dateRegex)
	z = time1Reg.search(text)
	if(z):
		hour = int(z.groups()[1])
		minute = 0
		matchedTime = time(hour, minute,00) 
	time2Reg = re.compile(g_dateRegex2)
	z = time2Reg.search(text)
	if(z):
		hour = int(z.groups()[0])
		minute = int(z.groups()[3])
		matchedTime = time(hour, minute,00) 
	return matchedTime
	

if __name__ == '__main__':
	if(DEBUG):
		import unittest
		unittest.main()   
	else:
		main()

