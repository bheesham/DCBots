# Copyright (C) 2011 Bheesham Persaud.
import httplib, urllib, re, cgi


# Setup
hubHost     = "carletonhub.ca"
hubPort     = 411               # default is 411 for most servers
botName     = "URLBot"
botPass     = ""
botOwner    = "Bonnie"

ignoreUsers	= [ "HubBot" ]
ignoreURLS  = [ "carletonhub.ca", "imgur.com", "google.", "goo.gl", "bit.ly", "t.co", "tinyurl.com", "facebook.com" ]

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
    
    URLPattern      = re.compile( "([a-zA-Z0-9\-\.]+)\.([a-zA-Z]+){2,3}(\S*)" )
    namePattern     = re.compile( botName )
    
    chat_buffer     = ""
    chat_buffer_l   = ""
    chat_commands   = []
    
    url             = ""
    page_contents   = ""
    begin_tag       = 0
    end_tag         = 0
    title           = ""
    ignoreMessage   = False
    
    infinite        = 1
    
    while ( infinite == 1 ):
        chat_buffer   = URLBot.get_buffer()
        chat_commands = URLBot.get_command( chat_buffer )
        
        matches       = URLPattern.search( chat_buffer )
        is_my_message = namePattern.search( chat_buffer )
        
        # Ignore users
        ignoreMessage = False
        for name in ignoreUsers:
            if chat_buffer.find( name ) > -1:
                ignoreMessage = True
        # Ignore the URL's
        for url in ignoreURLS:
            chat_buffer_l = chat_buffer.lower()
            if chat_buffer_l.find( url ) > -1:
                ignoreMessage = True
        
        if ( matches is not None and is_my_message is None and ignoreMessage is False and chat_commands == '$CHAT' ):
            try:
                url             = "http://" + matches.group(0)
                server          = urllib.urlopen( url )
                page_contents   = server.read()
                
                begin_tag   = page_contents.find("<title>")
                end_tag     = page_contents.find("</title>")
                
                if ( begin_tag != -1 and end_tag != -1 ):
                    begin_tag   = page_contents.split( "<title>" )
                    end_tag   = begin_tag[1].split( "</title>" )
                    title           = end_tag[0]
                    if ( len( title ) < 257 ):
                        title = title.replace( "$", "&#36;" )
                        title = title.replace( "|", "&#124;" )
                        title = title.replace( '  ', '' )
                        title = title.replace( '\n', '' )
                        title = title.replace( '\r', '' )
                    else:
                        title = title.replace( "$", "&#36;" )
                        title = title.replace( "|", "&#124;" )
                        title = title.replace( '  ', '' )
                        title = title.replace( '\n', '' )
                        title = title.replace( '\r', '' )
                        title = title[:256] + "..."
                    URLBot.send_chat_msg( title + " --- " + url )
                urllib.urlcleanup()
            except:
                pass
    pass
else:
    print "Could not log in. :("