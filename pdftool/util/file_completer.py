import os

from prompt_toolkit.completion import Completer, Completion


class FileCompleter(Completer):
    """
    This completer auto suggests files inside the current path the user has already typed.
    Similar like you know it from every CLI.
    """

    def __init__(self):
        self.cwd = '.'

    def get_completions(self, document, complete_event):
        prefix = document.text_before_cursor
        if '/' in prefix:
            self.cwd = os.path.dirname(prefix)
            prefix = os.path.basename(prefix)
        else:
            self.cwd = '.'

        if os.path.exists(self.cwd):
            for file_name in os.listdir(self.cwd):
                if file_name.startswith(prefix):
                    full_path = os.path.join(self.cwd, file_name)
                    if os.path.isdir(full_path):
                        file_name += '/'
                    yield Completion(file_name, start_position=-len(prefix))
