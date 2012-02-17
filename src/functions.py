# Copyright (C) 2011 Bheesham Persaud.

import HTMLParser

def unescape(text):
    return HTMLParser.HTMLParser().unescape( text )