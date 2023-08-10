import unittest
from router import *
from utils.models import PrefixNode
from utils.trie import SingleTrie, CombineTrie
from utils.data_sample import price_list_sample


class ModelTestCase(unittest.TestCase):
    def test_prefix_namedtuple(self):
        self.assertEqual(
            f"{PrefixNode('A', '1', 0.9)}", "(prefix: '1', operator: 'A', price: 0.9)"
        )
        self.assertEqual(
            f"{PrefixNode()}", "(prefix: '', operator: 'None', price: inf)"
        )


class TrieTestCase(unittest.TestCase):
    def test_create_single_trie(self):
        self.assertEqual(f"{SingleTrie()}", "PrefixNode({} -> {})")

    def test_create_combine_trie(self):
        self.assertEqual(f"{CombineTrie()}", "PrefixNode({} -> {})")


class FindCheapestPriceTestCase(unittest.TestCase):
    def test_init_trie(self):
        self.assertEqual(
            f"{init_trie(trie_type='single', price_data=price_list_sample)}",
            "{'A': PrefixNode({} -> {'1': PrefixNode({'A': (0.9, '1')} -> {}), '2': PrefixNode({} -> {'6': PrefixNode({} -> {'8': PrefixNode({'A': (5.1, '268')} -> {})})}), '4': PrefixNode({} -> {'6': PrefixNode({'A': (0.17, '46')} -> {'2': PrefixNode({} -> {'0': PrefixNode({'A': (0.0, '4620')} -> {})}), '8': PrefixNode({'A': (0.15, '468')} -> {}), '3': PrefixNode({} -> {'1': PrefixNode({'A': (0.15, '4631')} -> {})}), '7': PrefixNode({} -> {'3': PrefixNode({'A': (0.9, '4673')} -> {'2': PrefixNode({'A': (1.1, '46732')} -> {})})})})})}), 'B': PrefixNode({} -> {'1': PrefixNode({'B': (0.92, '1')} -> {}), '4': PrefixNode({} -> {'4': PrefixNode({'B': (0.5, '44')} -> {}), '6': PrefixNode({'B': (0.2, '46')} -> {'7': PrefixNode({'B': (1.0, '467')} -> {})}), '8': PrefixNode({'B': (1.2, '48')} -> {})})})}",
        )
        self.assertEqual(
            f"{init_trie(trie_type='combined', price_data=price_list_sample)}",
            "PrefixNode({} -> {'1': PrefixNode({'A': (0.9, '1'), 'B': (0.92, '1')} -> {}), '2': PrefixNode({} -> {'6': PrefixNode({} -> {'8': PrefixNode({'A': (5.1, '268')} -> {})})}), '4': PrefixNode({} -> {'6': PrefixNode({'A': (0.17, '46'), 'B': (0.2, '46')} -> {'2': PrefixNode({} -> {'0': PrefixNode({'A': (0.0, '4620')} -> {})}), '8': PrefixNode({'A': (0.15, '468')} -> {}), '3': PrefixNode({} -> {'1': PrefixNode({'A': (0.15, '4631')} -> {})}), '7': PrefixNode({'B': (1.0, '467')} -> {'3': PrefixNode({'A': (0.9, '4673')} -> {'2': PrefixNode({'A': (1.1, '46732')} -> {})})})}), '4': PrefixNode({'B': (0.5, '44')} -> {}), '8': PrefixNode({'B': (1.2, '48')} -> {})})})",
        )

    def test_single_trie(self):
        trie_dict = init_trie(trie_type="single", price_data=price_list_sample)
        self.assertEqual(
            find_cheapest_price_using_single_trie(trie_dict, "4673212345"),
            PrefixNode("B", "467", 1.0),
        )
        self.assertEqual(
            find_cheapest_price_using_single_trie(trie_dict, "44910283733"),
            PrefixNode("B", "44", 0.5),
        )
        self.assertEqual(
            find_cheapest_price_using_single_trie(trie_dict, "1234567890"),
            PrefixNode("A", "1", 0.9),
        )
        self.assertEqual(
            find_cheapest_price_using_single_trie(trie_dict, "2679187391"),
            None,
        )
        self.assertEqual(
            find_cheapest_price_using_single_trie(trie_dict, "84987654321"),
            None,
        )
        self.assertEqual(
            find_cheapest_price_using_single_trie(trie_dict, ""),
            None,
        )

    def test_mul_operator_combine_trie(self):
        trie = init_trie(trie_type="combined", price_data=price_list_sample)
        self.assertEqual(
            find_cheapest_price_using_combine_trie(trie, "4673212345"),
            PrefixNode("B", "467", 1.0),
        )
        self.assertEqual(
            find_cheapest_price_using_combine_trie(trie, "44910283733"),
            PrefixNode("B", "44", 0.5),
        )
        self.assertEqual(
            find_cheapest_price_using_combine_trie(trie, "1234567890"),
            PrefixNode("A", "1", 0.9),
        )
        self.assertEqual(
            find_cheapest_price_using_combine_trie(trie, "2679187391"),
            None,
        )
        self.assertEqual(
            find_cheapest_price_using_combine_trie(trie, "84987654321"),
            None,
        )
        self.assertEqual(
            find_cheapest_price_using_combine_trie(trie, ""),
            None,
        )


if __name__ == "__main__":
    unittest.main()
