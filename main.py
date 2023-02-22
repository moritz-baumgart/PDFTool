from merge import merge
from reorderDualPage import reorderDualPage
from deletePages import deletePages

from clintermission import CliMenu, CliMenuStyle, CliMenuCursor

def main():

    choices = {
        'Merge files': merge,
        'Reorder dual page scan': reorderDualPage,
        'Delete single pages': deletePages
    }

    style = CliMenuStyle('#CCCCCC', '#FFFFFF', '#FFFF00')
    menu = CliMenu(choices, "Time to choose:\n", dedent_selection=True, style=style, cursor=CliMenuCursor.ARROW)
    
    selection = menu.get_selection()[1]

    if(selection is not None):
        choices[selection]()





if __name__ == '__main__':
    main()

 

