from .console.server import ConsoleServer


class IrcConsoleServer(ConsoleServer):

    def __init__(self, target, server, port, nickname, client, on_disconnect=None):

        # Set up the properties we'll need in the run() method:
        #
        self.name = client._view.settings().get('name')
        self.server = server
        self.nickname = nickname
        self.on_disconnect = on_disconnect
        self.port = port
        self.target = target
        self._client = client
        self._write = client.write

        # Initialise the base class to kick off the thread:
        #
        ConsoleServer.__init__(self)

    def run(self):

        from .simple_irc_client.simple_irc_client import IRCClient

        self.irc = IRCClient(self._write, self.target, self.nickname, self._on_disconnect)
        try:
            self._write(u'*** Connecting to \'{0}:{1}\' with nickname \'{2}\''.format(self.server, self.port, self.nickname))
            self.irc.connect(self.server, 6667, self.nickname)
            self.irc.start()
        except Exception as x:   # client.ServerConnectionError, x:
            self._write(u'*** Error: {0}'.format(x))

    def execute(self, command):

        command = self._client.clean_command(command)
        if command:
            # Send the command to the IRC server:
            #
            self.irc.write(command)

            # Now echo the command to the display and clear the line ready for
            # the next command:
            #
            self._write('{0}: {1}'.format(self.nickname, command))
            self._client.clear_command_line()

    def _on_disconnect(self):

        if self.on_disconnect is not None:
            self.on_disconnect(self.name)
