import sublime

from .console.client import ConsoleClient


class IrcConsoleClient(ConsoleClient):
    """Create a console client specifically set up for IRC."""

    def __init__(self, name, view=None, data=None):

        # If there is no existing view then create a new buffer and
        # indicate that it's a scratch buffer:
        #
        # [TODO] Consider simply making this a saved log file. See issue #6.
        #
        if view is None:
            view = sublime.active_window().new_file()
            view.set_scratch(True)

        # Let the base class do its work:
        #
        ConsoleClient.__init__(self, name, view, client_type='IRC', data=data)
