import easydate
from datetime import *
import sys
import re

__doc__ = """  This module is for converting a to-do string into a 'todo' object.  Each todo 
object is a dictionary with a set of expected values

'starttime': a datetime object for when the  event starts
'endtime' : a datetime object for when the event ends
'calander' : a calendar name for the targetcalendar
'sourceCalander' : a calendar name for the targetcalendar. 'todo list' by default
'Locations' : a string indicating a location
'tags' : a dictionary of tags. Each tag is a 'tag:data' pair. Data can be a string or a tuple.

Examples: """

hashRegex = "#([a-zA-Z]*)(\(.*?\))?"
atRegex = "@([a-zA-Z]*)(\(.*?\))?"

def stripHashTags(todoItemString):
	""" takes a todo stirng. Removed the #tagname and #tagname(property) style hash tag.
	And stores them in a dictoary of {tagname:property} pairs. 
	Returns a tuple of the todo string (minus the matched tags) and a dictionary of tags, and
	their properties. """
	return  fastStrip(todoItemString, hashRegex)


def stripAtTags(todoItemString):
	""" takes a todo stirng. Removed the #tagname and @tagname(property) style hash tag.
	And stores them in a dictoary of {tagname:property} pairs. 
	Returns a tuple of the todo string (minus the matched tags) and a dictionary of tags, and
	their properties. """
	return  fastStrip(todoItemString, atRegex)


def fastStrip(todoItemString, hashRegex):
	hashtagsDict = {}
	removal = []
	reg = re.compile(hashRegex,re.I);
	
	# match all of the # tags that we can match
	for match in reg.finditer(todoItemString):
		group = match.groups()
#		print group
		hashtagsDict[group[0]] = group[1:] if len(group) >2 else group[1]
		removal.append( (match.start(),match.end()) )

	#remove the #tags from the input text
	removal.reverse()
	for (start,end) in removal:
		todoItemString = todoItemString[:start] + todoItemString[end:]
	return todoItemString.strip(), hashtagsDict


def todoTimeFromDate(dateObj):
	""" function creates a 'todo time' datetime object from a datetime.date. 
	If dateObj is today && current hour < 1300 a datetime object for 1300 today returns
	If dateObj is today, && 1300 < current hour < 2200 , a datetime object 2200 today returns
	If dateObj is today, otherwise a datetime object for 'now' returns. 
	If dateObj is NOT today, a datetime for 1300 on that date is returned
	"""
	if(dateObj == None):
		return None
		
	now = datetime.now()
	if(now.date() == dateObj):
		if(now.hour < 13):
			return datetime(now.year, now.month, now.day, 13,0,0)
		elif(now.hour < 22):
			return datetime(now.year, now.month, now.day, 22,0,0)
		return now()
	return datetime(dateObj.year, dateObj.month, dateObj.day,13,00, 00)	


def processAtTags(hashDict):

	# -- Convert date string into a dattime object
	if 'date' in hashDict.keys():
		text = str(hashDict['date']).lstrip("[{(").rstrip("]})")
		dateObj = easydate.getBestDateFromText(text)
		datetimeObj = todoTimeFromDate(dateObj)
		if(datetimeObj != None):
			hashDict['date'] = datetimeObj

	if 'cal' in hashDict.keys():
		#TODO: find if we can match an exiting or expected calander
#		print "cal match found: " + str(hashDict['cal'])
		pass
	
	#TODO: for everythign that isn't a keyword, look to see if we can math a location
		# with the todo list.
	return hashDict


def fullToDoItemFromText(todoItemString):
	#-- strip out @tags. These are simpler tags, and explicitly explain how to process themselves.
	todoItemString, hashDict = stripAtTags(todoItemString)
	
	print hashDict
	#-- process @tags, and make full objects/items out of them.
	hashDict = processAtTags(hashDict)
	# string out #tags.  These are 'smart' tags, and they try to intellegently expand and match
	# process #tags, and make full objects/items out of them.
	
	# return full objects to the caller
	return todoItemString, hashDict


def main():

	usageString = """ This is a command line interface for converting a 'todo' event into magic. Read the doc. """

	"""example: - Print out paperowrk @hive76 #tomorrow """
	# @XXXX -> interpert @ at a place, person, or resource needed
	# @date(tomorrow) -> interpert as date
	# @cal(calendar name) -> adds the event to that calendar

	# #tomorrow -> interpert text # as a date target 
	# #Home_Calander => Interperts text as calander name "Home Calander"
	# #(Home Calander) => Interperts text as calander name "Home Calander"
	# #'Home Calander' => Interperts text as calander name "Home Calander"
	
	
	if( len(sys.argv) == 1):
	 	print usageString
	else:	 	
		argString = ' '.join(sys.argv[1:])
		e = fullToDoItemFromText(argString)
		print "date computed is: " + str(e)


if __name__ == '__main__':
	main()

