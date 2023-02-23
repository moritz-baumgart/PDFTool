from sys import exit

from clintermission import CliMenu, CliMenuCursor, CliMenuStyle
from operations import delete_pages, merge, reorder_dual_page


def main():

    not_done = True
    while not_done:

        choices = {
            'Merge files': merge,
            'Reorder dual page scan': reorder_dual_page,
            'Delete single pages': delete_pages,
            'Exit': exit
        }

        # Prompt the user a kind of "main menu" with the options above
        style = CliMenuStyle('#CCCCCC', '#FFFFFF', '#FFFF00')
        menu = CliMenu(choices, "\nWhat do you want to do?:\n", dedent_selection=True, style=style, cursor=CliMenuCursor.ARROW)

        selection = menu.get_selection()[1]

        if selection is not None:
            # call the function associated with this selection.
            # By convention the operations return True on abort. So we stay inside the loop if the user only aborted, otherwise we exit the loop and the script terminates
            not_done = choices[selection]()
        else:
            # if selection is none the user pressed e.g. ctrl+c, exit at this point
            not_done = False


if __name__ == '__main__':
    main()
