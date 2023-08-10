"""
author: @linhpduc
"""
import sys
import time
import random
from router import *
from utils.data_sample import price_list_sample


def main_combine_trie(numbers, test_perf: bool = False):
    start = time.time()
    trie = init_trie(trie_type="combined", price_data=price_list_sample)
    prices = [
        find_cheapest_price_using_combine_trie(trie=trie, number=number)
        for number in numbers
    ]
    if not test_perf:
        print(f"Results: \n\t{prices}")
    elapsed = time.time() - start
    print("Combine Trie:")
    print(f"\t+time elapsed: {elapsed:.6f}s")
    print(f"\t+size of trie: {sys.getsizeof(trie)} bytes")
    print("-"*50)


def main_single_trie(numbers, test_perf: bool = False):
    start = time.time()
    trie_dict = init_trie(trie_type="single", price_data=price_list_sample)
    prices = [
        find_cheapest_price_using_single_trie(trie_dict=trie_dict, number=number)
        for number in numbers
    ]
    if not test_perf:
        print(f"Results: \n\t{prices}")
    elapsed = time.time() - start
    print("Single Trie:")
    print(f"\t+time elapsed: {elapsed:.6f}s")
    print(f"\t+size of trie: {sys.getsizeof(trie_dict)} bytes")
    print("-"*50)


def main_test_perf():
    numbers = [str(random.randint(1_000_000_000, 9_999_999_9999)) for _ in range(1_000_000)]
    main_single_trie(numbers, test_perf=True)
    main_combine_trie(numbers, test_perf=True)


if __name__ == "__main__":
    # main_single_trie(sys.argv[1:])
    main_combine_trie(sys.argv[1:])
    # main_test_perf()
