#
# The best way to make this work is to treat the window as a document.
#
# This allows the user to do Sublime-like things, such as selecting many items and
# submitting them as a group to an IRC server.
#
# However, it means that the command prompt is not a prompt as such, but a marker
# to help us find the end of the document.
#
import sys
from imp import reload

import sublime
import sublime_plugin

from IRC.utils import get_setting

from .irc_client.irc_console_broker import IrcConsoleBroker

mod_prefix = 'IRC'

for suffix in ['.irc_client.irc_console_broker', '.irc_client.irc_console_client', '.irc_client.irc_console_server', '.irc_client.console.client', '.irc_client.console.server']:
    mod = mod_prefix + suffix
    reload(sys.modules[mod])


# Keep track of the brokers:
#
brokers = {}


class IrcCommand(sublime_plugin.WindowCommand):

    def on_disconnect(self, name):

        if name in brokers:
            del brokers[name]

    def run(self, target, server=None, port=None, name=None, nickname=None):

        # Ensure that the target has a hash at the beginning:
        #
        if target[0] != '#':
            target = '#' + target

        # Get any default values for the server and port from the config file,
        # if necessary:
        #
        if server is None:
            server = get_setting('server')

        if port is None:
            port = get_setting('port', 6667)

        # If no name is provided then make one up from server, port and target:
        #
        if name is None:
            name = '{0}:{1}{2}'.format(server, port, target)

        # Get the nickname from the config file if not provided:
        #
        if nickname is None:
            nickname = get_setting('nickname')

            # If we still have no nickname then ask the OS:
            #
            if nickname is None:
                import getpass

                nickname = getpass.getuser()

        # Wire up a command client and server:
        #
        brokers[name] = IrcConsoleBroker(name, target, view=None, server=server, port=port, nickname=nickname)


class IrcListener(sublime_plugin.EventListener):

    def on_activated_async(self, view):

        settings = view.settings()
        data = settings.get('data', None)
        if data is not None:
            name = settings.get('name', None)
            if name is not None and name not in brokers:
                brokers[name] = IrcConsoleBroker(name, data['target'], view=view, server=data['server'], port=data['port'], nickname=data['nickname'])


# The command that is executed when [ENTER] is pressed:
#
class CommitMsgCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # Use the buffer name to work out which set of settings we're
        # using:
        #
        broker = brokers[self.view.settings().get('name')]

        # Grab any regions, and use them to run the command:
        #
        for region in self.view.sel():
            if region.empty():
                region = self.view.line(region)
            command = self.view.substr(region)

            # Now execute the command:
            #
            broker.execute(command)


# The command that is executed to insert text into the current window:
#
class InsertTextCommand(sublime_plugin.TextCommand):

    def run(self, edit, pos, msg):

        self.view.insert(edit, pos, msg)


# The command that is executed to erase text in the current window:
#
class EraseTextCommand(sublime_plugin.TextCommand):

    def run(self, edit, a, b):

        self.view.erase(edit, sublime.Region(a, b))
