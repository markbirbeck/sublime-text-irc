from .irc_console_client import IrcConsoleClient
from .irc_console_server import IrcConsoleServer


class IrcConsoleBroker(object):

    def __init__(self, name, target, view=None, server=None, port=None, nickname=None, on_disconnect=None):

        # Wire up a console client and server:
        #
        data = {
            'target': target,
            'server': server,
            'port': port,
            'nickname': nickname
        }
        self._client = IrcConsoleClient(name, view=view, data=data)
        self._server = IrcConsoleServer(target, server, port, nickname, self._client, on_disconnect)

    def execute(self, command):

        self._server.execute(command)
