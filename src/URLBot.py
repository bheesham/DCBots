# Copyright (C) 2011 Bheesham Persaud.
import httplib, urllib, re


# Setup
hubHost     = "carletonhub.ca"
hubPort     = 411               # default is 411 for most servers
botName     = "URLBot"
botPass     = ""
botOwner    = "Bonnie"

# No need to edit the below.
from DCBot import DCBot

URLBot          = DCBot( hubHost, hubPort, botName, botPass, botOwner )
URLBot.debug    = False

URLBot.login()

class DiffUserAgent(urllib.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2"
urllib._urlopener = DiffUserAgent()



if ( URLBot.logged_in == True ):
    # Now that it's logged in, we can compile the Regular
    # Expressions to save some time.
    
    URLPattern      = re.compile( "([a-zA-Z0-9\-\.]+)\.([a-zA-Z]+){2,3}(\S*)", re.M )
    TitlePattern    = re.compile( "<title>(.*)</title>", re.M )
    namePattern     = re.compile( botName, re.M )
    
    chat_buffer     = ""
    chat_commands   = []
    
    url             = ""
    page_contents   = ""
    title           = ""
    
    infinite        = 1
    
    while ( infinite == 1 ):
        chat_buffer   = URLBot.get_buffer()
        matches       = URLPattern.search( chat_buffer )
        is_my_message = namePattern.search( chat_buffer )
        if ( matches is not None and is_my_message is None ):
            try:
                url             = "http://" + matches.group(0)
                server          = urllib.urlopen( url )
                page_contents   = server.read()
                title           = TitlePattern.search( page_contents )
                if ( title is not None ):
                    title           = title.group(1)
                    URLBot.send_chat_msg( "Title: " + title + " --- URL: " + url )
                urllib.urlcleanup()
            except:
                pass
    pass
else:
    print "Could not log in. :("