"""
author: @linhpduc
"""
import sys
from typing import Any, Dict
from abc import ABC, abstractmethod
from utils import PriceItem
from utils.trie import Trie


class Router(ABC):
    @abstractmethod
    def find_cheapest_price_by(self, number: str):
        pass

    @abstractmethod
    def get_size(self):
        pass


class SimpleRouter(Router):
    def __init__(self, price_data: Dict) -> None:
        self.trie_dict = {}
        for operator, price_list in price_data.items():
            self.trie_dict[operator] = Trie()
            self.trie_dict[operator].load_prices(
                operator=operator, price_list=price_list
            )

    def find_cheapest_price_by(self, number: str) -> Any:
        cheapest = PriceItem()
        for operator, trie in self.trie_dict.items():
            result = trie.search(number)  # {'A': (1.1, '467')}
            if len(result) > 0 and result[operator][0] < cheapest.price:
                cheapest = PriceItem(operator, result[operator][1], result[operator][0])
        return cheapest if cheapest.operator else None

    def get_size(self):
        return sys.getsizeof(self.trie_dict)


class AdvancedRouter(Router):
    def __init__(self, price_data: Dict) -> None:
        self.trie = Trie()
        for operator, price_list in price_data.items():
            self.trie.load_prices(operator=operator, price_list=price_list)

    def find_cheapest_price_by(self, number: str) -> Any:
        cheapest = PriceItem()
        result = self.trie.search(number)  # {'A': (1.1, '467'), 'B': (1.0, '46732')}
        for operator, (price, prefix) in result.items():
            if price < cheapest.price:
                cheapest = PriceItem(operator, prefix, price)
        return cheapest if cheapest.operator else None

    def get_size(self):
        return sys.getsizeof(self.trie)


class InvalidRunningMode(ValueError):
    pass


def router_factory(data: Dict, mode: str = "advanced") -> Router:
    match mode:
        case "simple":
            return SimpleRouter(price_data=data)
        case "advanced":
            return AdvancedRouter(price_data=data)
        case _:
            raise InvalidRunningMode(mode)
