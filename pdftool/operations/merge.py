import os
import pathlib
from typing import List

from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import ProgressBar
from PyPDF2 import PdfMerger, PdfReader
from util import FileCompleter, constants, create_cli_menu


def merge() -> bool:

    file_paths: List[pathlib.Path] = []
    not_done = True
    while not_done:

        # print the currently selected files above the prompt
        if len(file_paths) == 0:
            selectedFiles = 'No files selected!'
        else:
            selectedFiles = ', '.join([file.name for file in file_paths])

        # the choices the user has in this "submenu"
        choices = [
            'Add a file/directory',
            'MERGE!',
            'Abort'
        ]

        # prompt one of the choices above
        menu = create_cli_menu(choices, f'\n● MERGE\nSelected files: { selectedFiles }\n')
        selection = menu.get_selection()
        # selection is none if user presses e.g. ctrl+c, exit at this point
        if selection[0] is None:
            exit()

        # choices 0-2 correspond to choices above
        elif selection[0] == 0:

            # prompt user for a file/dir to be added, check existence
            file = prompt('\nEnter a file or directory (leave empty for current directory): ', completer=FileCompleter(), style=constants.PROMPT_STYLE).strip()
            path = pathlib.Path(file).absolute()
            if path.exists():
                file_paths.append(path)
            else:
                print('File does not exist! Ignoring.')
        elif selection[0] == 1:

            # prompt output file name, if none given use default, then call __merge
            output_file = prompt('\nEnter output file name (leave empty for default \'merge-output.pdf\'): ', style=constants.PROMPT_STYLE).strip()
            if len(output_file) == 0:
                output_file = 'merge-output.pdf'

            output_file_path = pathlib.Path(output_file)
            if output_file_path.exists():
                menu = create_cli_menu(['Abort!', 'OVERWRITE!'], '\nFile already exists!', style=constants.CLI_MENU_STYLE_ERROR)
                selection = menu.get_selection()[0]
                if selection is None or selection == 0:
                    return True

            __merge(file_paths, output_file_path)
            return False
        elif selection[0] == 2:
            # return true on abort so main nows we aborted and does not exit
            return True


def __merge(file_paths: List[pathlib.Path], output_file_name: str) -> None:
    '''
    Merges the given files into a single one and writes the result into the given output file.
    Checks if file are of type PDF. If a directory is found, it scans inside for PDFs and uses them.
    Wraps beautiful progress bars around everything.
    '''

    all_pdf_paths: List[pathlib.Path] = []

    with patch_stdout():
        with ProgressBar(title='Scanning files...') as p_b:
            for fp in p_b(file_paths):
                # check if file and pdf
                if fp.is_file():
                    if fp.suffix == '.pdf':
                        all_pdf_paths.append(fp)
                        print(f'Added: {fp}')
                    else:
                        print(f'Not a PDF: {fp}')
                # if directory, scan for pdfs in the dir
                elif fp.is_dir():
                    print(f'Found directory! Searching PDFs in: {fp}')
                    for fpd in [pathlib.Path(os.path.join(fp, file)) for file in os.listdir(fp)]:
                        if fpd.is_file():
                            if fpd.suffix == '.pdf':
                                all_pdf_paths.append(fpd)
                                print(f'Found PDF! Added: {fpd}')

    with patch_stdout():
        # use pypdf2 pdf merger to merge the pdfs
        merger = PdfMerger()
        with ProgressBar(title='Merging...') as p_b:
            for fp in p_b(all_pdf_paths):
                print(f'Appending: {fp}')
                merger.append(PdfReader(fp))

        print('Saving result...')
        merger.write(output_file_name)
