import unittest
from router import mul_operator_mul_trie, mul_operator_combine_trie
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
        self.assertEqual(
            f"{SingleTrie()}", "PrefixNode({} -> {})"
        )

    def test_create_combine_trie(self):
        self.assertEqual(
            f"{CombineTrie()}", "PrefixNode({} -> {})"
        )


class FindCheapestPriceTestCase(unittest.TestCase):
    def test_mul_operator_mul_trie(self):
        self.assertEqual(
            mul_operator_mul_trie(price_list_sample, "4673212345"),
            PrefixNode("B", "467", 1.0),
        )
        self.assertEqual(
            mul_operator_mul_trie(price_list_sample, "44910283733"),
            PrefixNode("B", "44", 0.5),
        )
        self.assertEqual(
            mul_operator_mul_trie(price_list_sample, "1234567890"),
            PrefixNode("A", "1", 0.9),
        )
        self.assertEqual(
            mul_operator_mul_trie(price_list_sample, "2679187391"),
            None,
        )
        self.assertEqual(
            mul_operator_mul_trie(price_list_sample, "84987654321"),
            None,
        )
        self.assertEqual(
            mul_operator_mul_trie(price_list_sample, ""),
            None,
        )

    def test_mul_operator_combine_trie(self):
        self.assertEqual(
            mul_operator_combine_trie(price_list_sample, "4673212345"),
            PrefixNode("B", "467", 1.0),
        )
        self.assertEqual(
            mul_operator_combine_trie(price_list_sample, "44910283733"),
            PrefixNode("B", "44", 0.5),
        )
        self.assertEqual(
            mul_operator_combine_trie(price_list_sample, "1234567890"),
            PrefixNode("A", "1", 0.9),
        )
        self.assertEqual(
            mul_operator_combine_trie(price_list_sample, "2679187391"),
            None,
        )
        self.assertEqual(
            mul_operator_combine_trie(price_list_sample, "84987654321"),
            None,
        )
        self.assertEqual(
            mul_operator_combine_trie(price_list_sample, ""),
            None,
        )


if __name__ == "__main__":
    unittest.main()
