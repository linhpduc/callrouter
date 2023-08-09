"""
The main function to run the program
"""
import sys
from models import PrefixNode
from trie import SingleTrie, CombineTrie
from data_sample import price_list_sample


def mul_operator_mul_trie(number):                  # "4673212345"
    # Init data structure and load data into tries
    trie_dict = {}
    for operator, price_list in price_list_sample.items():
        trie_dict[operator] = SingleTrie()
        trie_dict[operator].load_price_into_trie(
            operator=operator, price_list=price_list
        )

    # Determine the cheapest price
    cheapest = PrefixNode()
    for operator, trie in trie_dict.items():
        result = trie.search(number)                # iter 1: {'A': (1.1, '46732')}; iter 2: {'B': (1.0, '467')}
        if len(result) > 0 and result[operator][0] < cheapest.price:
            cheapest = PrefixNode(
                operator=operator,
                prefix=result[operator][1],
                price=result[operator][0],
            )
    return cheapest if cheapest.operator else None  # (prefix='467', operator='B', price=1.0)


def mul_operator_combine_trie(number):              # "4673212345"
    # Init data structure and load data into tries
    trie = CombineTrie()
    for operator, price_list in price_list_sample.items():
        trie.load_price_into_trie(operator=operator, price_list=price_list)

    # Determine the cheapest price
    cheapest = PrefixNode()
    result = trie.search(number)                    # {'A': (1.1, '46732'), 'B': (1.0, '467')}
    for operator, (price, prefix) in result.items():
        if price < cheapest.price:
            cheapest = PrefixNode(
                operator=operator,
                prefix=result[operator][1],
                price=result[operator][0],
            )
    return cheapest if cheapest.operator else None  # (prefix='467', operator='B', price=1.0)


def find_cheapest_price_by(number, func=mul_operator_combine_trie):
    return func(number)


if __name__ == "__main__":
    numbers = sys.argv[1:]
    prices = [find_cheapest_price_by(number) for number in numbers]
    print(prices)
