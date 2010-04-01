from EasyDate import *

class TestClass(unittest.TestCase):
	def testDateByDelta(self):
		tmDT = datetime.today() + timedelta(days=1)
		baseDate = tmDT.date()
		testDate = dateByDelta()		
		test2Date = dateByDelta(1)
		test3Date = dateByDelta(daysInTheFuture=1)	
		self.assertEqual(baseDate, testDate,'badly generated datetime object for dateByDelta')
		self.assertEqual(baseDate, test2Date,'badly generated datetime object for dateByDelta')		
		self.assertEqual(baseDate, test3Date,'badly generated datetime object for dateByDelta')
		pass


	def testDatetimeByTextToday(self):
		baseDate = datetime.today().date()
		testDate = dateByFutureDayText('today')
		self.compareDates(baseDate, testDate,'badly generated datetime object for today')
		test2Date = dateByFutureDayText('Today')
		self.compareDates(baseDate, test2Date,'badly generated datetime object for Today ')		
	
	def testDatetimeByTextTomorrow(self):
		tmDT = datetime.today() + timedelta(days=1)
		baseDate = tmDT.date()
		testDate = dateByFutureDayText('tomorrow')
		self.compareDates(baseDate, testDate,'badly generated datetime object for today')
		test2Date = dateByFutureDayText('Tomorrow')
		self.compareDates(baseDate, test2Date,'badly generated datetime object for Today ')		

	def compareDates(self,dateBase,date2,textError):
		self.assertEquals(dateBase.year,date2.year,textError + " (year error)")
		self.assertEquals(dateBase.month,date2.month,textError + " (month error)")
		self.assertEquals(dateBase.day,date2.day,textError + " (minute error)")


if __name__ == "__main__":
	import unittest
	unittest.main()   
