from prompt_toolkit import prompt
from util import FileCompleter

def merge():
    
    p = prompt('Test', completer=FileCompleter())
    print(p)
