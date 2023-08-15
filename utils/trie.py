"""
author: @linhpduc
"""
from typing import List, Dict, Tuple
from utils import PriceItem


class Trie:
    def __init__(self):
        self.next = {}
        self.price_dict = {}

    def __repr__(self):
        return f"Trie({self.price_dict} -> {self.next})"

    def insert(self, data: PriceItem) -> None:
        curr_node = self
        for edge in str(data.prefix):
            if edge not in curr_node.next:
                curr_node.next[edge] = Trie()
            curr_node = curr_node.next[edge]
        curr_node.price_dict |= {data.operator: (data.price, data.prefix)}

    def load_prices(self, operator: str, price_list: List[Tuple[str, float]]) -> None:
        for prefix, price in price_list:
            self.insert(data=PriceItem(operator, prefix, price))
        # print(f"loaded {len(price_list)} items from operator '{operator}'.")

    def search(self, number: str) -> Dict:
        curr_node = self
        price_dict = {}
        for edge in str(number):
            if edge not in curr_node.next:
                break
            curr_node = curr_node.next[edge]
            if len(curr_node.price_dict) > 0:
                price_dict |= curr_node.price_dict
        return price_dict
