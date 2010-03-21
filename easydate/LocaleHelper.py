class LocaleHelper(object):
    """ This class is used to store a locale, and the date patters associated
    with that locale.  Based on the instance local, or the passed 'locale' variable,
    it returns various regex lookup strings to indicate what order, laugauge, or type of string
    to expect for using in smart conversion

    Example:
    >>> pattern = LocaleHelper('en')
    >>> pattern.date(None)
    'Y M D'    
    >>> pattern.time(None)
    'H M'    
    >>> pattern.date('de')
    'D M Y'

    TODO: Add more patterns
    """
    __date_I = 'Y M D'
    __date_II = 'D M Y'
    __date_III = 'M D Y'
    __time_I = 'H M'
    __time_II = 'M H' # ever used ??

    PATTERNS = {
        'date': dict(),
        'time': dict(),
    }
    
    PATTERNS['date']['iso'] = __date_I
    PATTERNS['time']['iso'] = __time_I

    for locale in ['de', 'de-de', 'de-at', 'de-ch', 'es', 'fr', 'uk', 'it', 'cs']:
        PATTERNS['date'][locale] = __date_II
    
    for locale in ['en']:
        PATTERNS['date'][locale] = __date_III
    
    for locale in ['en', 'de', 'de-de', 'de-at', 'de-ch', 'es', 'fr', 'uk',
                   'it', 'cs']:
        PATTERNS['time'][locale] = __time_I


    defaultLocale = 'en'
    knownLocals = ['en','de']

    def __init__(self, localeString=None):
	""" creates an instance of the object. If a localeString is specified, later call to the object
	will use that locale as the default, if passed local string matches an entry in knownLocales"""
	if localeString == None:
		self.defaultLocale = 'en' #default to english. I know sad 'eh?
	elif localeString.lower() in knownLocals:
		self.defaultLocale = localeString.lower()
    
    def datePattern(self,locale=None):
	""" Function returns a string listing the expected date pattern based on the current locale.

	if(locale == None):
		locale = self.defaultLocale
	elif localeString.lower() not in knownLocals:
		return "" #no match!
	return self.PATTERNS['date'].get(locale, self.__date_I)

    
    def timePattern(self,locale=None):
	""" Function returns a string listing the expected time pattern based on the current locale.
	Returns None on error """
	if(locale == None):
		locale = self.defaultLocale
	elif localeString.lower() not in knownLocals:
		return None #no match!
        return self.PATTERNS['time'].get(locale, self.__time_I)



