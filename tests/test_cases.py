import unittest
from router import *
from utils import PriceItem
from utils.trie import Trie
from utils.data_sample import price_list_sample


class PriceItemTestCase(unittest.TestCase):
    def test_prefix_namedtuple(self):
        self.assertEqual(
            f"{PriceItem('A', '1', 0.9)}", "(prefix: '1', operator: 'A', price: 0.9)"
        )
        self.assertEqual(f"{PriceItem()}", "(prefix: '', operator: 'None', price: inf)")


class TrieTestCase(unittest.TestCase):
    def test_trie_init(self):
        self.assertEqual(f"{Trie()}", "Trie({} -> {})")

    def test_trie_insert(self):
        t = Trie()
        p1 = PriceItem("A", "849", 0.4)
        t.insert(p1)
        self.assertEqual(
            f"{t}",
            "Trie({} -> {'8': Trie({} -> {'4': Trie({}"
            " -> {'9': Trie({'A': (0.4, '849')} -> {})})})})",
        )
        p2 = PriceItem("B", "84", 0.8)
        t.insert(p2)
        self.assertEqual(
            f"{t}",
            "Trie({} -> {'8': Trie({} -> {'4': Trie({'B': "
            "(0.8, '84')} -> {'9': Trie({'A': (0.4, '849')} -> {})})})})",
        )
        p3 = PriceItem("B", "849", 0.6)
        t.insert(p3)
        self.assertEqual(
            f"{t}",
            "Trie({} -> {'8': Trie({} -> "
            "{'4': Trie({'B': (0.8, '84')} -> "
            "{'9': Trie({'A': (0.4, '849'), 'B': (0.6, '849')} -> {})})})})",
        )

    def test_trie_search(self):
        t = Trie()
        for o, p_list in price_list_sample.items():
            t.load_prices(operator=o, price_list=p_list)
        self.assertEqual(
            t.search("4673212345"), {"A": (1.1, "46732"), "B": (1.0, "467")}
        )
        self.assertEqual(t.search("44910283733"), {"B": (0.5, "44")})
        self.assertEqual(t.search("1234567890"), {"A": (0.9, "1"), "B": (0.92, "1")})
        self.assertEqual(t.search("2679187391"), {})
        self.assertEqual(t.search("84987654321"), {})
        self.assertEqual(t.search(""), {})


class RouterTestCase(unittest.TestCase):
    def test_router_simple(self):
        r = SimpleRouter(price_data=price_list_sample)
        self.assertEqual(r.get_size(), 232)
        self.assertEqual(
            r.find_cheapest_price_by("4673212345"), PriceItem("B", "467", 1.0)
        )
        self.assertEqual(r.find_cheapest_price_by("89373822722"), None)
        self.assertEqual(r.find_cheapest_price_by("24628273929"), None)
        self.assertEqual(
            r.find_cheapest_price_by("11282739293"), PriceItem("A", "1", 0.9)
        )
        self.assertEqual(
            r.find_cheapest_price_by("4429283473473"), PriceItem("B", "44", 0.5)
        )
        self.assertEqual(r.find_cheapest_price_by(""), None)

    def test_router_advanced(self):
        r = AdvancedRouter(price_data=price_list_sample)
        self.assertEqual(r.get_size(), 48)
        self.assertEqual(
            r.find_cheapest_price_by("4673212345"), PriceItem("B", "467", 1.0)
        )
        self.assertEqual(r.find_cheapest_price_by("89373822722"), None)
        self.assertEqual(r.find_cheapest_price_by("24628273929"), None)
        self.assertEqual(
            r.find_cheapest_price_by("11282739293"), PriceItem("A", "1", 0.9)
        )
        self.assertEqual(
            r.find_cheapest_price_by("4429283473473"), PriceItem("B", "44", 0.5)
        )
        self.assertEqual(r.find_cheapest_price_by(""), None)

    def test_router_factory(self):
        self.assertTrue(
            isinstance(
                router_factory(data=price_list_sample, mode="simple"), SimpleRouter
            )
        )
        self.assertTrue(
            isinstance(
                router_factory(data=price_list_sample, mode="advanced"), AdvancedRouter
            )
        )
        self.assertRaises(
            InvalidRunningMode, router_factory, price_list_sample, "supersaiyan"
        )
        self.assertTrue(issubclass(Router, ABC))
        self.assertRaises(TypeError, Router)


if __name__ == "__main__":
    unittest.main()
