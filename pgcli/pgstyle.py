from __future__ import unicode_literals

import pygments.styles
from pygments.token import string_to_tokentype
from pygments.style import Style as PygmentsStyle
from pygments.util import ClassNotFound
from prompt_toolkit.styles.pygments import style_from_pygments_cls, style_from_pygments_dict
from prompt_toolkit.styles import merge_styles, Style


def style_factory(name, cli_style):
    try:
        style = pygments.styles.get_style_by_name(name)
    except ClassNotFound:
        style = pygments.styles.get_style_by_name('native')

    custom_styles = {}
    for token in cli_style:
        try:
            custom_styles[string_to_tokentype(
                token)] = style.styles[string_to_tokentype(cli_style[token])]
        except AttributeError as err:
            custom_styles[string_to_tokentype(token)] = cli_style[token]

    override_style = Style([('bottom-toolbar', 'noreverse')])
    return merge_styles([
        style_from_pygments_cls(style),
        style_from_pygments_dict(custom_styles),
        override_style
    ])


def style_factory_output(name, cli_style):
    try:
        style = pygments.styles.get_style_by_name(name).styles
    except ClassNotFound:
        style = pygments.styles.get_style_by_name('native').styles

    for token in cli_style:
        try:
            style.update({string_to_tokentype(
                token): style[string_to_tokentype(cli_style[token])], })
        except AttributeError as err:
            style.update(
                {string_to_tokentype(token): cli_style[token], })

    class OutputStyle(PygmentsStyle):
        default_style = ""
        styles = style

    return OutputStyle
