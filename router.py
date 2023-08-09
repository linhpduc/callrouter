"""
author: @linhpduc
"""

from typing import Callable, Any
from utils.models import PrefixNode
from utils.trie import SingleTrie, CombineTrie


def mul_operator_mul_trie(price_data: dict, number: str) -> Any:
    # Init data structure and load data into tries
    trie_dict = {}
    for operator, price_list in price_data.items():
        trie_dict[operator] = SingleTrie()
        trie_dict[operator].load_price_into_trie(
            operator=operator, price_list=price_list
        )

    # Determine the cheapest price
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


def mul_operator_combine_trie(price_data: dict, number: str) -> Any:
    # Init data structure and load data into tries
    trie = CombineTrie()
    for operator, price_list in price_data.items():
        trie.load_price_into_trie(operator=operator, price_list=price_list)

    # Determine the cheapest price
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


def find_cheapest_price_by(
    price_data: dict, number: str, func: Callable = mul_operator_combine_trie
) -> Any:
    return func(price_data, number)
