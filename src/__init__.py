# Copyright (C) 2011 Bheesham Persaud.

# Setup
hubHost     = ""
hubPort     = 411               # default is 411 for most servers
botName     = "IdleDC"
botPass     = ""
botOwner    = ""

# No need to edit the below.
from DCBot import DCBot

IdleDC          = DCBot( hubHost, hubPort, botName, botPass, botOwner )
IdleDC.debug    = True

IdleDC.login()

IdleDC.send_chat_msg( "Hey guys, this is Bheesham's bot. This is a test message. If you see this then everything is going according to plan." )