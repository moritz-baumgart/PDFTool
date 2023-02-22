from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit.patch_stdout import patch_stdout
from clintermission import CliMenu, CliMenuStyle, CliMenuCursor
import pathlib
from typing import List
import os
from PyPDF2 import PdfReader, PdfMerger

from util import FileCompleter



def merge() -> bool:

    file_paths: List[pathlib.Path] = []
    not_done = True
    while not_done:
        choices = [
            'Add a file/directory',
            'MERGE!',
            'Abort'
        ]

        style = CliMenuStyle('#CCCCCC', '#FFFFFF', '#FFFF00')

        if len(file_paths) == 0:
            selectedFiles = 'No files selected!'
        else:
            selectedFiles = ', '.join([file.name for file in file_paths])

        menu = CliMenu(choices, f'\n● MERGE\nSelected files: { selectedFiles }\n', dedent_selection=True, style=style, cursor=CliMenuCursor.ARROW)
        selection = menu.get_selection()
        if selection[0] is None:
            exit()
        elif selection[0] == 0:
            file = prompt('\nEnter a file or directory (leave empty for current directory): ', completer=FileCompleter())
            path = pathlib.Path(file).absolute()
            if path.exists():
                file_paths.append(path)
            else:
                print('File does not exist! Ignoring.')
        elif selection[0] == 1:
            output_file = prompt('\nEnter output file name (leave empty for default \'merge-output.pdf\'): ')
            if len(output_file) == 0:
                output_file = 'merge-output.pdf'
            __merge(file_paths, output_file)
            return False
        elif selection[0] == 2:
            return True
    



def __merge(file_paths: List[pathlib.Path], output_file_name: str) -> None:

    all_pdf_paths: List[pathlib.Path] = []

    with patch_stdout():
        with ProgressBar(title='Scanning files...') as pb:
            for fp in pb(file_paths):
                if fp.is_file():
                    if fp.suffix == '.pdf':
                        all_pdf_paths.append(fp)
                        print(f'Added: {fp}')
                    else:
                        print(f'Not a PDF: {fp}')
                elif fp.is_dir():
                    print(f'Found directory! Searching PDFs in: {fp}')
                    for fpd in [pathlib.Path(file) for file in os.listdir()]:
                        if fpd.is_file():
                            if fpd.suffix == '.pdf':
                                all_pdf_paths.append(fpd)
                                print(f'Found PDF! Added: {fp}')

    with patch_stdout():
        merger = PdfMerger()
        with ProgressBar(title='Merging...') as pb:
            for fp in pb(all_pdf_paths):
                print(f'Appending: {fp}')
                merger.append(PdfReader(fp))

        print('Saving result...')
        merger.write(output_file_name)
