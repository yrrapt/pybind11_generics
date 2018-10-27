# -*- coding: utf-8 -*-

from typing import List


def get_help_strs(obj: object) -> List[str]:
    return obj.__doc__.splitlines()
