"""
author: @linhpduc
"""

from typing import Any
from utils.models import PrefixNode
from utils.trie import SingleTrie, CombineTrie


def init_trie(trie_type: str, price_data: dict) -> Any:
    if trie_type == "combined":
        trie = CombineTrie()
        for operator, price_list in price_data.items():
            trie.load_price_into_trie(operator=operator, price_list=price_list)
        return trie
    else:
        trie_dict = {}
        for operator, price_list in price_data.items():
            trie_dict[operator] = SingleTrie()
            trie_dict[operator].load_price_into_trie(
                operator=operator, price_list=price_list
            )
        return trie_dict


def find_cheapest_price_using_single_trie(trie_dict: dict[str: SingleTrie], number: str) -> Any:
    cheapest = PrefixNode()
    for operator, trie in trie_dict.items():
        result = trie.search(number)
        if len(result) > 0 and result[operator][0] < cheapest.price:
            cheapest = PrefixNode(
                operator=operator,
                prefix=result[operator][1],
                price=result[operator][0],
            )
    return cheapest if cheapest.operator else None


def find_cheapest_price_using_combine_trie(trie: CombineTrie, number: str) -> Any:
    cheapest = PrefixNode()
    result = trie.search(number)
    for operator, (price, prefix) in result.items():
        if price < cheapest.price:
            cheapest = PrefixNode(
                operator=operator,
                prefix=result[operator][1],
                price=result[operator][0],
            )
    return cheapest if cheapest.operator else None
