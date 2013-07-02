import threading


class ConsoleServer(threading.Thread):

    def __init__(self):

        # Get ready for threading:
        #
        threading.Thread.__init__(self)

        # Kick off the thread:
        #
        self.start()

    def execute(self, command):

        return command
