"""
author: @linhpduc
"""
import sys
from router import find_cheapest_price_by
from utils.data_sample import price_list_sample

if __name__ == "__main__":
    numbers = sys.argv[1:]
    prices = [
        find_cheapest_price_by(price_data=price_list_sample, number=number)
        for number in numbers
    ]
    print(prices)
