from tododate import *

import unittest

class TestToDoMagic(unittest.TestCase):
	
	def testStripHashTags(self):
		tests = (
			("todo test #foo #bar #baz(time and stuff)", "todo test", { 'baz':'(time and stuff)','foo':None, 'bar':None}),		
		)
		for (fullString,expectedToDo,expectedDict) in tests:
			todo,hashtagDict = stripHashTags(fullString)
			self.assertEqual(expectedToDo,todo,"mismatched todo string after hash stripped '" + str(todo)+"'")
			self.assertEqual(expectedDict,hashtagDict, str(hashtagDict))
	
	def testStripAtTags(self):
		tests = (
			("todo test @foo @bar @baz(time and stuff)", "todo test", { 'baz':'(time and stuff)','foo':None, 'bar':None}),		
			("todo test @home @dave @date(2010.03.12)", "todo test", { 'date':'(2010.03.12)','home':None, 'dave':None}),	
			("eat @date(tuesday the 20th) @home @cal(events)","eat",{'date':'(tuesday the 20th)','home':None,'cal':'(events)'}),
		)
		for (fullString,expectedToDo,expectedDict) in tests:
			todo,tagsDict = stripAtTags(fullString)
			self.assertEqual(expectedToDo,todo,"mismatched todo string after hash stripped '" + str(todo)+"'")
			self.assertEqual(expectedDict,tagsDict, "match fail "+ str(expectedDict) + " src: "+str(tagsDict) + " todo: "+str(todo) )

	def testProcessAtTags(self):
		tests = (
			{ 'date':'(2010.03.12)','home':None, 'dave':None},		
			{ 'cal':'(Home Calendar)','home':None, 'dave':None},		
			{ 'cal':'(Home Cal)','home':None, 'dave':None},		
			{ 'cal':'(Home)','home':None, 'dave':None},		
		)
		for hashDict in tests:
			newHashDict = processAtTags(hashDict)
			#print newHashDict

#	def testFullToDoItemFromText(self):
#		tests = (
#			("todo test @home @dave @date(2010.03.12)", "todo test", { 'date':'(2010.03.12)','home':None, 'dave':None}),		
#		)
#		for (fullString,expectedToDo,expectedDict) in tests:
#			todo,hashtagDict = fullToDoItemFromText(fullString)
#			self.assertEqual(expectedToDo,todo,"mismatched todo string after hash stripped '" + str(todo)+"'")
#			self.assertEqual(expectedDict,hashtagDict, str(hashtagDict))

if __name__ == "__main__":
		unittest.main()   
