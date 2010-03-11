import unittest
import sys
from os import path
DEBUG = False

class TestToDoFind(unittest.TestCase):
	
	def testThing(self):
		pass;


def main():
	print 'hello world'
	argv = sys.argv[1:]

	if(len(argv) < 2):
		print "usage is 'filename hashtag'"
		return None
	todoListFind(argv[0],argv[1:])

def todoListFind(filename, tagsList):
	""" takes a file name and a list of tags to search for,
	searches the file for matching todo entries and returns them"""
	fh = open(path.expanduser(filename),'r')
	text = fh.read()
	lines = text.split('\n')
	for tag in tagsList:
		#matches = simpleTagMatch(tag,lines)
		matches = smarterTagMatch(tag,lines)
		printMatches(tag,matches)

def printMatches(tag,matchesList):
	print "matches found for tag", str(tag), ":",str(len(matchesList))
	for match in matchesList:
		print "\t" + match	

def smarterTagMatch(tag, linesList):
	"""Smarter tag matche that scans for 
	'-' starting a line, and raw text in each line."""
	matches = [line for line in linesList if str(tag) in line]
	matches = [line for line in matches if line.strip()[0] == '-']
	return matches	

def simpleTagMatch(tag, linesList):
	"""Naive tag matche that simply scans for raw text in each line."""
	matches = [line for line in linesList if str(tag) in line]
	return matches	

if __name__ == '__main__':
	
	if(DEBUG):
		unittest.main()
	main();
