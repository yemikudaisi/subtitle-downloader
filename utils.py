import sys


def string_to_query(text):
    if sys.version.startswith('2.'): # for Python 2 version
        import urllib
        return urllib.quote_plus(text)
    else:
        import urllib.parse
        return urllib.parse.parse_qs(text)
