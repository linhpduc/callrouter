"""
author: linhpduc
"""
import math
from typing import NamedTuple


class PrefixNode(NamedTuple):
    operator: str = None
    prefix: str = ""
    price: float = math.inf

    def __repr__(self):
        return f"(prefix: '{self.prefix}', operator: '{self.operator}', price: {self.price})"
