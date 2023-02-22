from PyInquirer import prompt
from merge import merge
from reorderDualPage import reorderDualPage
from deletePages import deletePages

def main():

    choices = {
        '- Merge files': merge,
        '- Reorder dual page scan': reorderDualPage,
        '- Delete single pages': deletePages
    }

    question = [
        {
            'type': 'list',
            'name': 'operation',
            'message': 'What do you want to do?',
            'choices': choices.keys()
        }
    ]

    operation = prompt(question)['operation']
    choices[operation]()


if __name__ == '__main__':
    main()


