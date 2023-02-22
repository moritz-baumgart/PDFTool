from clintermission import CliMenu, CliMenuStyle, CliMenuCursor
from sys import exit

from operations import merge, reorderDualPage, deletePages

def main():


    not_done = True

    while not_done:

        choices = {
            'Merge files': merge,
            'Reorder dual page scan': reorderDualPage,
            'Delete single pages': deletePages,
            'Exit': exit
        }

        style = CliMenuStyle('#CCCCCC', '#FFFFFF', '#FFFF00')
        menu = CliMenu(choices, "\nWhat do you want to do?:\n", dedent_selection=True, style=style, cursor=CliMenuCursor.ARROW)
        
        selection = menu.get_selection()[1]

        if(selection is not None):
            not_done = choices[selection]()
        else:
            not_done = False

if __name__ == '__main__':
    main()
