# Copyright (C) 2011 Bheesham Persaud.

# Setup
hubHost     = "carletonhub.ca"
hubPort     = 411               # default is 411 for most servers
botName     = "IdleDC"
botPass     = ""
botOwner    = "Bonnie"

# No need to edit the below.
from DCBot import DCBot

IdleDC          = DCBot( hubHost, hubPort, botName, botPass, botOwner )
IdleDC.debug    = True

IdleDC.login()

if ( IdleDC.logged_in == True ):
    pass
    # IdleDC.send_chat_msg( "Hey guys, this is Bonnie's bot. This is a test message. If you see this then everything is going according to plan." )
    # Initiate an infinite loop and add something along the lines of hooks
else:
    print "Could not log in. :("