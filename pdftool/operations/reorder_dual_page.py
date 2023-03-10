import pathlib

from prompt_toolkit import HTML, print_formatted_text, prompt
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import ProgressBar
from pypdf import PdfReader, PdfWriter
from util import FileCompleter, constants, create_cli_menu


def reorder_dual_page():
    '''
    Prompts for input file, reorders its pages (see comment at the end) and writes it to prompted output file.
    Return True on abort, False on success
    '''

    # prompt the user for a filename with the style above
    file = prompt('\n● REORDER DUAL PAGE\nEnter a file: ', completer=FileCompleter(), style=constants.PROMPT_STYLE).strip()

    # if no name given, abort
    if len(file) == 0:
        print_formatted_text(HTML('<ansired>\nFile name empty! Aborting.</ansired>'))
        return True

    # if file does not exist, abort
    path = pathlib.Path(file)
    if not path.exists():
        print_formatted_text(HTML('<ansired>\nFile does not exist! Aborting.</ansired>'))
        return True

    # if number of pages odd, abort
    reader = PdfReader(path)
    page_num = len(reader.pages)
    if page_num % 2 != 0:
        print_formatted_text(HTML('<ansired>\nNumber of pages in the document is odd! Aborting.</ansired>'))
        return True

    # prompt for an output file name with style, if none is given use default
    output_file_name = prompt('\nEnter output file name (leave empty for default \'reorder-output.pdf\'): ', completer=FileCompleter(), style=constants.PROMPT_STYLE).strip()
    if len(output_file_name) == 0:
        output_file_name = 'reorder-output.pdf'

    output_file_path = pathlib.Path(output_file_name)
    if output_file_path.exists():
        menu = create_cli_menu(['Abort!', 'OVERWRITE!'], '\nFile already exists!', style=constants.CLI_MENU_STYLE_ERROR)
        selection = menu.get_selection()[0]
        if selection is None or selection == 0:
            return True

    # reorder the pages and write result with progress bar
    # reordering happens in the following fashion:
    # p1f, p2f, p3f, ..., p3b, p2b, p1b, ... => p1f, p1b, p2f, p2b, p3f, p3b, ...
    with patch_stdout():
        writer = PdfWriter()
        half = page_num // 2
        with ProgressBar(title='Reordering...') as p_b:
            for i in p_b(range(half)):
                writer.add_page(reader.pages[i])
                writer.add_page(reader.pages[page_num - i - 1])

        print('Saving result...')
        writer.write(output_file_path)

    return False
