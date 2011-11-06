# Copyright (C) 2011 Bheesham Persaud.
class DCBot:
    """A class to handle all the needed bot functions."""
    
    def __init__( self, host, port, nick, passw ):
        """Initialize the bot. If the passw parameter is set then the bot will attempt to log into the server."""
        self.host   = host
        self.port   = port
        self.nick   = nick
        self.passw  = passw