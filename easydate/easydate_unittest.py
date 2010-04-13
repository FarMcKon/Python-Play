from easydate import *

__author__ = "Far McKon"
__maintainer__ = "Far McKon"
__email__ = "FarMcKon@gmail.com"
__copyright__ = "Copyright 2010, Far McKon Bespoke Industries"
__license__ = "GPL"
__version__ = "0.1.1.0"
__code_uuid__ = "78e6e643-c4e7-4bc0-bf64-6e427bfd4a3a"

__docformat__ = "restructuredtext"
__doc__ =  """ This is a unittest module for easydate """


_manualChecks = []


class EasyDateUnitTests(unittest.TestCase):
	""" Main test class for easydate unit tests"""

	def testWeekdayNumberByName(self):
		""" test the weekday index by name of the day function"""
		# -- test full names
		testList = [(s, daysOfTheWeek.index(s)) for s in daysOfTheWeek]
		for name,expected in testList:
			weekdayIndex = weekdayNumberByName(name)
			self.assertEqual(weekdayIndex, expected, "name of the day didn't match expected offset "
			+ str(weekdayIndex) + " " +str(expected) + " "+name  )
		
		# -- test long abbr
		daysOfTheWeekAbbr = ['Mon','Tues','Wed','Thurs','Fri', 'Sat','Sun']
		testList = [(s, daysOfTheWeekAbbr.index(s)) for s in daysOfTheWeekAbbr]
		for name,expected in testList:
			weekdayIndex = weekdayNumberByName(name)
			self.assertEqual(weekdayIndex, expected, "name of the day didn't match expected offset "
			+ str(weekdayIndex) + " " +str(expected) + " "+name  )

		# -- test short abbr
		daysOfTheWeekAbbr = ['mon','Tu','wed','th','fri', 'sat','sun']
		testList = [(s, daysOfTheWeekAbbr.index(s)) for s in daysOfTheWeekAbbr]
		for name,expected in testList:
			weekdayIndex = weekdayNumberByName(name)
			self.assertEqual(weekdayIndex, expected, "name of the day didn't match expected offset "
			+ str(weekdayIndex) + " " +str(expected) + " "+name  )

	def testNumberFromDatOFMonth(self):
		""" test the weekday index by name of the day function"""
		tests = ("12th",12),("13",13),("22nd",22),("3rd",3),("3",3),("5",5)
		for test,expected in tests:
			found = numberFromDayOFMonth(test)
			self.assertEqual(found, expected, "Did not find number" + str(expected) + " in date string: "+test)

	def testDateByDelta(self):
		""" Unit test for creating a datetime.date object by a date delta"""
		tmDT = datetime.today() + timedelta(days=1)
		baseDate = tmDT.date()
		testDate = dateByDelta()		
		test2Date = dateByDelta(1)
		test3Date = dateByDelta(daysInTheFuture=1)	
		self.assertEqual(baseDate, testDate,'badly generated datetime object for dateByDelta')
		self.assertEqual(baseDate, test2Date,'badly generated datetime object for dateByDelta')		
		self.assertEqual(baseDate, test3Date,'badly generated datetime object for dateByDelta')
		pass

	def testDateByTextToday(self):
		""" Unit test for creating a datetime.date object by the word 'today'"""
		baseDate = datetime.today().date()
		testDate = dateByFutureDayName('today')
		self.compareDates(baseDate, testDate,'badly generated datetime object for today')
		test2Date = dateByFutureDayName('Today')
		self.compareDates(baseDate, test2Date,'badly generated datetime object for Today ')		
	
	def testDateByTextTomorrow(self):
		""" Unit test for creating a datetime.date object by the word 'tomorrow''"""
		tmDT = datetime.today() + timedelta(days=1)
		baseDate = tmDT.date()
		testDate = dateByFutureDayName('tomorrow')
		self.compareDates(baseDate, testDate,'badly generated datetime object for today')
		test2Date = dateByFutureDayName('Tomorrow')
		self.compareDates(baseDate, test2Date,'badly generated datetime object for Today ')		

	def testDateByNextDayNameExpectFailure(self):
		""" Unit test for creating a datetime.date object by matching a date name 'today'"""
		daysOfTheWeekAbbr = ['MonDog','Tuesad','Wedding']
		for dayname in daysOfTheWeekAbbr:
			testDate = dateByFutureDayName(dayname)
			self.assertEqual(testDate,None, "matched a date badly for " + dayname)

	def testDateByNextDayName(self):
		""" Unit test for creating a datetime.date object by matching a date name 'today'"""

		_manualChecks.append("This test is for the next 'dayname' match. It requires a manual match")

		for dayname in daysOfTheWeek:
			testDate = dateByFutureDayName(dayname)
			_manualChecks.append(("check that this is the next "+dayname,testDate))
		daysOfTheWeekAbbr = ['Mon','Tues','Wed','Thur','Thurs','Fri', 'Sat','Sun','mon','Tu','wed','th','fri', 'sat','sun']
		for dayname in daysOfTheWeekAbbr:
			testDate = dateByFutureDayName(dayname)
			_manualChecks.append(("check that this or next "+dayname,testDate))

		for line in _manualChecks:
			print line
		
	def testDateByLastDayName(self):
		print "This test is for the next 'day and number' match. It requires a manual match."
		import datetime
		# Tricky: These date tests are only valid around march 2010. you will need to rewrite them.
		#"tested 2010.04.12 and worked."
		if(datetime.datetime.now().date() <= datetime.datetime(2010,04,13).date()):
			self.assertTrue(False,"These tests only are valid on 2010.04.13. Please update these tests")	

		testList = ("Thursday the 15th", 2010,04,15),("Tuesday the 20th", 2010,04,20), ("Tu the 13 ",2010,04,13), 
			("Saturday the 1st",2010,05,01), ("Tuesday the 1st",2010,06,01)

		for string, year,month,day in testList:			
			testDate = dateByNameAndDayNumber(string)
			self.assertEquals(testDate, datetime.datetime(year,month,day).date(), 
				"string date of "+ string + "and numerical date don't match: " + str((year,month,day)))

	def compareDates(self,dateBase,date2,textError):
		self.assertEquals(dateBase.year,date2.year,textError + " (year error)")
		self.assertEquals(dateBase.month,date2.month,textError + " (month error)")
		self.assertEquals(dateBase.day,date2.day,textError + " (minute error)")



if __name__ == "__main__":
	import unittest
	unittest.main()   
	if(len(_manualChecks) > 0):
		print "Manual Checks Required for:"
		for check in _manualChecks:
			print check
