# -*- coding: utf-8 -*-

"""."""

import re


_UNIT_STRING_REGEX = r'^([0-9\.]+)(ml|cl|dl|l)$'


def parse_unit(unit_string):
    """."""
    lower_unit_string = unit_string.lower()
    match = re.match(_UNIT_STRING_REGEX, lower_unit_string)

    if match:
        try:
            return float(match.group(1)), match.group(2)
        except ValueError:
            return None, None
    else:
        return None, None
