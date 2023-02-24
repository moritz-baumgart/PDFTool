'''
This file contains util function.
'''

from clintermission import CliMenu, CliMenuCursor

from . import constants


def create_cli_menu(choices, question, style=constants.CLI_MENU_STYLE, cursor=CliMenuCursor.ARROW):
    '''
    Creates and return a CliMenu with default or given style and cursor and the given choices/question
    '''
    return CliMenu(choices, question, dedent_selection=True, style=style, cursor=cursor)
