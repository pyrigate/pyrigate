# -*- coding: utf-8 -*-

"""."""

import colorise

from pyrigate.user_settings import settings


def print_dict(
    dictionary,
    name_format='{0}{{fg=white,bold}}{1:<{2}}{{reset}}{3}',
    value_format='{0:>{1}}',
    indent='    ',
    buffer=' ' * 5
):
    """Recursively print a dictionary with indentation."""
    def _print_dict(
        dictionary,
        name_format,
        value_format,
        indent,
        lvl=0,
        buffer=' '
    ):
        l_indent = indent * lvl

        # Find the max key and value widths for proper alignment
        max_key_width = len(max(dictionary.keys(), key=len))
        max_value_width = len(
            max(dictionary.values(), key=lambda v: len(str(v)))
        )

        for key, value in dictionary.items():
            if not value:
                continue

            if isinstance(value, dict):
                colorise.fprint(
                    '{0}{{fg=white,bold}}{1}{{reset}}'.format(l_indent, key),
                    enabled=settings['colors']
                )
                _print_dict(
                    value,
                    name_format,
                    value_format,
                    indent,
                    lvl=lvl+1,
                    buffer=buffer
                )
            elif isinstance(value, list):
                colorise.fprint(
                    name_format.format(
                        l_indent,
                        key,
                        max_key_width,
                        buffer
                    ),
                    enabled=settings['colors'],
                    end=''
                )

                print(value_format.format(', '.join(value), max_value_width))
            else:
                colorise.fprint(
                    name_format.format(
                        l_indent,
                        key,
                        max_key_width,
                        buffer
                    ),
                    enabled=settings['colors'],
                    end=''
                )
                print(value_format.format(value, max_value_width))

    _print_dict(dictionary, name_format, value_format, indent, buffer=buffer)


def print_list(rows, min_width=10, padding=5):
    """."""
    max_entry_width = max(
        min_width,
        max(len(str(entry)) for entry, _ in rows)
    ) + padding

    for entry, value in rows:
        colorise.fprint(
            f'{{fg=white,bold}}{str(entry):<{max_entry_width}}{{reset}}',
            end=''
        )

        print(f'{str(value)}')


def print_columns(rows, headers=None, min_width=10, padding=5):
    """Print dictionary keys and values in two columns."""
    if not rows:
        return

    if any(len(row) != len(rows[0]) for row in rows):
        raise ValueError('Length of rows must match')

    # Find the maximum widths for each column
    row_widths = [[len(str(elem)) for elem in row] for row in rows]

    if len(rows) > 1:
        max_column_widths = list(map(max, *row_widths))
    else:
        max_column_widths = row_widths[0]

    if headers:
        if len(headers) != len(rows[0]):
            raise ValueError('Header length must be length of rows')

        for header, mw in zip(headers, max_column_widths):
            colorise.fprint(
                f'{{fg=white,bold}}{header:<{mw+padding}}{{reset}}',
                end=''
            )

        print()

    for row in rows:
        for idx in range(len(row)):
            print(f'{str(row[idx]):<{max_column_widths[idx]+padding}}', end='')

        print()
