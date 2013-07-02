# A console client creates a view that will show a prompt at the end. When text
# is inserted it is placed just before the prompt, shifting the prompt down.
#
import sublime


class ConsoleClient(object):

    def __init__(self, name, view, client_type=None, data=None, prompt=None):

        # If there is no prompt then make one from the prefix:
        #
        if prompt is None:
            prompt = (client_type if client_type else '') + '>'

        # Add a space to the prompt:
        #
        if prompt[-1] != ' ':
            prompt += ' '

        self.prompt = prompt

        # Keep track of the buffer:
        #
        self._view = view

        # If a command type has been passed then add it to the caption and
        # load a syntax parser:
        #
        if client_type is not None:
            caption = "{0}: {1}".format(client_type, name)
            self._view.set_syntax_file('Packages/{0}/syntax/{0}.tmLanguage'.format(client_type))
        else:
            caption = name

        # Set the view's caption, save the name and show the prompt:
        #
        self._view.set_name(caption)
        self._view.settings().set('name', name)
        self.show_prompt(prompt)

        # Save any attached data:
        #
        if (data is not None):
            self._view.settings().set('data', data)

    def _erase(self, region):

        self._view.run_command('erase_text', {'a': region.a, 'b': region.b})

    def _write(self, pos, msg):

        self._view.run_command('insert_text', {'pos': pos, 'msg': msg})

    def clean_command(self, command, prompt=None):
        """Ensure that the command doesn't contain the prompt."""

        if prompt is None:
            prompt = self.prompt

        return command[len(prompt) if command.find(prompt) == 0 else 0:]

    def clear_command_line(self, prompt=None):
        """Clear the command entry area."""

        if prompt is None:
            prompt = self.prompt

        # Create a region that runs from the end of the prompt to the
        # end of the buffer:
        #
        region = sublime.Region(
            self.find_prompt(prompt).end(),
            self._view.size()
        )

        # Clear the region and move the cursor to the end:
        #
        self._erase(region)
        self._view.run_command('move_to', {'to': 'eof', 'extend': False})

    def show_prompt(self, prompt=None):
        """Display a prompt at the end of the buffer."""

        if prompt is None:
            prompt = self.prompt

        # Only insert the prompt if we don't have one already:
        #
        if self.find_prompt(prompt) == sublime.Region(-1, -1):
            self._write(0, prompt)

    def find_prompt(self, prompt=None):
        """Find the prompt."""

        if prompt is None:
            prompt = self.prompt

        return self._view.find('^{0}'.format(prompt), 0)

    def write(self, msg):

        # Add the message just before the prompt:
        #
        region = self.find_prompt()
        if region is None:
            pos = 0
        else:
            line = self._view.line(region)
            pos = line.begin()

        self._write(pos, msg + '\n')
