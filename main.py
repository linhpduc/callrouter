"""
author: @linhpduc
"""
import sys
import time
import random
from router import router_factory, InvalidRunningMode
from utils.data_sample import price_list_sample


def search_in_bulk(numbers: list, mode: str, test_perf: bool = False):
    print(f"[MODE={mode.upper()}]")
    start = time.time()
    router_instance = router_factory(data=price_list_sample, mode=mode)
    results = [
        router_instance.find_cheapest_price_by(number=number) for number in numbers
    ]
    elapsed = time.time() - start
    if not test_perf:
        print(f"- results: {results}")
    print(f"- time elapsed: {elapsed:.6f}s")
    print(f"- size of trie(s): {router_instance.get_size()} bytes")
    print("-" * 32)


def main():
    try:
        search_in_bulk(mode=sys.argv[1], numbers=sys.argv[2:])
    except InvalidRunningMode as e:
        print(f"'{e}': INVALID RUNNING MODE.")


def evaluate_perf():
    numbers = [
        str(random.randint(1_000_000_000, 9_999_999_9999)) for _ in range(1_000_000)
    ]
    search_in_bulk(numbers=numbers, mode="simple", test_perf=True)
    search_in_bulk(numbers=numbers, mode="advanced", test_perf=True)


if __name__ == "__main__":
    main()
    # evaluate_perf()
