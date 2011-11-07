# Copyright (C) 2011 Bheesham Persaud.

import socket, array, time, string, sys

class DCBot:
    """A class to handle all the needed bot functions."""
    
    # Default values
    host            = ""        # Hub IP
    port            = 411       # What port to connect on?
    nick            = ""        # Nickname / display name
    passw           = ""        # Password for authentication
    owner           = ""        # Who controls this bot?
    
    # From below this comment, the user will have to manually change the
    # values for the variables they so wish to change.
    
    # For these values, the user will have to manually change them.
    debug           = False
    client          = "DCBot"
    version         = "0.0.1"
    
    # User related values
    description     = "A friendly bot made for human service."
    email           = "bheesham123@hotmail.com"
    connection      = "LAN(T1)"
    share_size      = 0         # How much data shared in kB.
    
    # Server related values
    server_socket   = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # The socket we'll use to talk with the server
    nick_list       = []        # A list of all connected users
    op_list         = []        # A list of all Operators
    logged_in       = False
    
    def __init__( self, host, port, nick, passw, owner ):
        """Initialize the bot. If the passw parameter is set then the bot will attempt to log into the server."""
        self.host   = host
        self.port   = port
        self.nick   = nick
        self.passw  = passw
        self.owner  = owner
    
    def login(self):
        """Log into a server"""
        # Create a connection to the server
        self.server_socket.connect( ( self.host, self.port ) )
        if ( self.debug == True ): print "[DEBUG]Connection established."
        
        infinite    = True
        command     = ""
        buff        = ""
        
        self.send_msg( "$Hello, world|" )
        
        # Now we enter an infinite loop! Well, infinite until we log in
        # or something horrible happens.
        while ( infinite ):
            buff = self.get_buffer()
            if ( self.debug == True ): print buff
            if ( buff != "" ):
                command = self.get_command( buff )
                
                if ( command[0] == "Lock" ):
                    if ( self.debug == True ): print "[DEBUG]Server does not support $NoHello"
                    self.send_msg( "$Key " + self.lock2key( command[1] ) + "|" )
                    self.send_msg( "$ValidateNick " + self.nick + "|")
                elif ( command[0] == "UserIP" ):
                    if ( self.debug == True ): print "[DEBUG]Got $UserIP"
                elif ( command[0] == "Hello" ):
                    self.send_msg( "$Version " + self.version + "|" )
                    self.send_msg( "$MyINFO $ALL " + 
                                    self.nick + " " + 
                                    self.client + "$ $" + 
                                    self.version + "$" + 
                                    self.email + "$" + 
                                    str( self.share_size ) + "$|" )
                elif ( command[0] == "HubTopic" ):
                    if ( self.debug == True ): print "[DEBUG]Logged in"
        return 1
    
    def mainloop(self):
        pass
    
    def get_buffer(self):
        """Get the received content from a socket."""
        buff = ""
        self.server_socket.settimeout(0.13)
        while ( 1 ):
            try:
                while ( 1 ):
                    tmp = self.server_socket.recv( 1 )  # Receive 1 character at a time.
                    if ( tmp != "|" ):
                        buff += tmp
                    else:
                        return buff
            except socket.timeout:
                pass
            except socket.error, ( value, message ):
                if ( self.debug == True ): print "[DEBUG]Socket error: " + message
                sys.exit( 1 )
        # Just in case the socket times out or anything.
        return buff
    
    def get_command( self, bstring ):
        """Will check to see if a string has a command in it."""
        if ( bstring[:1] == '<' ):
            return '$CHAT'
        elif ( bstring[:1] != '$' ):
            return 0
        tmp = bstring[1:-1]
        return tmp.split()
    
    def lock2key(self, lock ): 
        """If a server requires a lock string, then this function will generate it."""
        lock = array.array( 'B', lock )
        lockLength  = len( lock )
        lockReply   = ""
        h = 0
        a = 0
        for j in xrange( lockLength ):
            if ( j == 0 ):
                h = lock[ j ] ^ lock[-1] ^ lock[-2] ^ 5
            else:
                h = lock[ j ] ^ lock[ j - 1 ]
            
            a = ( ( h << 4 ) | ( h >> 4 ) ) & 255
            
            if ( a == 126 or a == 124 or a == 96 or a == 36 or a == 0 ):
                lockReply = lockReply + "/%DCN"
                if ( a < 100 ): lockReply = lockReply + 0
                if ( a < 10 ):  lockReply = lockReply + 0
                lockReply = a + "%/" 
            else:
                lockReply = lockReply + chr( a )
        return lockReply
    
    def send_msg(self, msg):
        """Sends a message through the socket."""
        self.server_socket.send( msg )
        if ( self.debug == True ): print "[DEBUG]Sent: " + msg
        return True

    def send_chat_msg(self, msg):
        """Sends a message to chat."""
        self.send_msg( "<" + self.nick + "> " + msg + "|" )
