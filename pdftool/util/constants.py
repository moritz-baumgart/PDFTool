from prompt_toolkit.styles import Style
from clintermission import CliMenuStyle

PROMPT_STYLE = Style.from_dict({
    'prompt': 'ansiyellow'
})

CLI_MENU_STYLE = CliMenuStyle('#CCCCCC', '#FFFFFF', '#FFFF00')
CLI_MENU_STYLE_ERROR = CliMenuStyle('#CCCCCC', '#FFFFFF', '#FF0000')
