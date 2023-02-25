import pathlib
import re

from prompt_toolkit import HTML, print_formatted_text, prompt
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import ProgressBar
from pypdf import PdfReader, PdfWriter
from util import FileCompleter, constants, create_cli_menu


def delete_pages():
    '''
    Prompts the user for a document and pages to delete.
    Deletes the given pages by index and either overwrites the original or saves it in a new file.
    '''

    # prompt the user for a filename with the style above
    file = prompt('\n● DELETE SINGLE PAGES\nEnter a file: ', completer=FileCompleter(), style=constants.PROMPT_STYLE).strip()

    # if no name given, abort
    if len(file) == 0:
        print_formatted_text(HTML('<ansired>\nFile name empty! Aborting.</ansired>'))
        return True

    # if file does not exist, abort
    path = pathlib.Path(file)
    if not path.exists():
        print_formatted_text(HTML('<ansired>\nFile does not exist! Aborting.</ansired>'))
        return True

    # if file is not a pdf, abort
    if path.suffix != '.pdf':
        print_formatted_text(HTML('<ansired>\nFile name is not a PDF! Aborting.</ansired>'))
        return True

    # open the file
    print_formatted_text(HTML('<ansiyellow>\nReading file...</ansiyellow>'))
    reader = PdfReader(path)

    # prompt the user pages to delete
    page_indices = prompt('\nEnter the indices of pages to delete (starting at 1): ', completer=FileCompleter(), style=constants.PROMPT_STYLE).strip()

    # if none given, abort
    if len(page_indices) == 0:
        print_formatted_text(HTML('<ansired>\nNo page numbers given! Aborting.</ansired>'))
        return True

    # regex that matches numbers with any number of digits
    number_regex = re.compile(r'\d+')

    # find all numbers in the given input using the regex
    # this way the user can enter them the way they want
    # e.g. '1, 5, 7 8;9; 10: 12' would be valid
    page_indices_to_delete = number_regex.findall(page_indices)

    # convert to tuple to eliminate duplicates and parse the strings to ints
    page_indices_to_delete = {int(x) for x in page_indices_to_delete}

    # check if all indices or out of the bound of the pdf
    is_inside = False
    for page_num in page_indices_to_delete:
        if page_num < len(reader.pages):
            is_inside = True

    # ...if so, abort
    if not is_inside:
        print_formatted_text(HTML(f'<ansired>\nThe file only has { len(reader.pages) } pages! All given indices are out of bounds! Aborting.</ansired>'))
        return True

    # give a warning, when some indices are out of bound and prompt whether or not we should continue
    if len(reader.pages) < max(page_indices_to_delete):
        menu = create_cli_menu(
            ['Abort!', 'YES!'], f'\nThe file only has { len(reader.pages) } pages!\nAre you sure you want to continue? The indices out of bounds will be ignored.', style=constants.CLI_MENU_STYLE_ERROR)
        selection = menu.get_selection()[0]
        if selection is None or selection == 0:
            return True

    # prompt for an output file, if none is given overwrite input
    output_file_name = prompt('\nEnter output file name (leave empty to overwrite input file): ', completer=FileCompleter(), style=constants.PROMPT_STYLE).strip()
    output_path = pathlib.Path(output_file_name)
    if len(output_file_name) == 0:
        output_path = path

    if path == output_path:
        # if overwriting is chosen give one final prompt so the user can confirm their input
        menu = create_cli_menu(['Abort!', 'PROCEED!'],
                               f'\nBy proceeding the original file will be OVERWRITTEN: { path }:\nPages that will be deleted: { ", ".join([str(x) for x in page_indices_to_delete]) }', style=constants.CLI_MENU_STYLE_ERROR)
        selection = menu.get_selection()[0]
        if selection is None or selection == 0:
            return True
    elif output_path.exists():
        # else if the files already exits give a warning
        menu = create_cli_menu(['Abort!', 'OVERWRITE!'], '\nFile already exists!', style=constants.CLI_MENU_STYLE_ERROR)
        selection = menu.get_selection()[0]
        if selection is None or selection == 0:
            return True

    # copy all pages that should not be deleted and then write the new file
    writer = PdfWriter()
    with patch_stdout():
        with ProgressBar(title='Copying...') as p_b:
            for index, page in p_b(enumerate(reader.pages, 1), total=len(reader.pages)):
                if index not in page_indices_to_delete:
                    writer.add_page(page)

    print('Saving result...')
    writer.write(output_path)

    return False
