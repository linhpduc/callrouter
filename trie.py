"""
author: @linhpduc
"""

from abc import ABC, abstractmethod
from models import PrefixNode


class Trie(ABC):
    """
    Prefix trie
    """

    def __init__(self):
        self.next = {}
        self.price_dict = {}

    def __repr__(self):
        return f"PrefixNode({self.price_dict} -> {self.next})"

    def insert(self, node: PrefixNode) -> None:
        """
        Insert a node into trie. If same prefix from same operator, keep last price value.
        Example:
        - PrefixNode(next={}, price_dict={'A': (1.1, '46732')})
        """
        curr_node = self
        for edge in str(node.prefix):
            if edge not in curr_node.next:
                curr_node.next[edge] = self.get_instance()
            curr_node = curr_node.next[edge]
        curr_node.price_dict |= {node.operator: (node.price, node.prefix)}

    def load_price_into_trie(
        self, operator: str, price_list: list[tuple[str, float]]
    ) -> None:
        for prefix, price in price_list:
            self.insert(node=PrefixNode(operator, prefix, price))

    @abstractmethod
    def search(self, number: str) -> dict:
        pass

    @abstractmethod
    def get_instance(self):
        pass


class SingleTrie(Trie):
    """
    A separate trie for each operator
    """

    def search(self, number: str) -> dict:
        """
        With each operator, find the longest matched prefix node
        """
        curr_node = self
        for edge in str(number):
            if edge not in curr_node.next:
                break
            curr_node = curr_node.next[edge]
        return curr_node.price_dict

    def get_instance(self):
        return SingleTrie()


class CombineTrie(Trie):
    """
    Combine prices of all operators into only one trie
    """

    def search(self, number: str) -> dict:
        """
        Find the price for longest prefix each operator
        """
        curr_node = self
        # Keep the price of longest matched prefix for each operator
        price_dict = {}
        for edge in str(number):
            if edge not in curr_node.next:
                break
            curr_node = curr_node.next[edge]
            if len(curr_node.price_dict) > 0:
                price_dict |= curr_node.price_dict
        return price_dict

    def get_instance(self):
        return CombineTrie()
