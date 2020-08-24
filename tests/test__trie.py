"""
.. py:module:: test_patricia
   :synopsis: Test cases for the PATRICIA trie implementation.

.. moduleauthor:: Florian Leitner <florian.leitner@gmail.com>
.. License: Apache License v2 (http://www.apache.org/licenses/LICENSE-2.0.html)
"""
from unittest import main, TestCase
from patricia import Trie, _NonTerminal

__author__ = "Florian Leitner"
__version__ = 9


class TrieTests(TestCase):
    def testInitContains(self) -> None:
        T = Trie(key=1)
        T = Trie(**T)
        self.assertTrue("key" in T)
        self.assertFalse("keys" in T)
        self.assertFalse("ke" in T)
        self.assertFalse("kex" in T)

    def testSetGetDel(self) -> None:
        T = Trie()
        T["foo"] = 1
        T["bar"] = 2
        T["baz"] = 3
        self.assertTrue("foo" in T)
        self.assertTrue("bar" in T)
        self.assertTrue("baz" in T)
        self.assertEqual(T["foo"], 1)
        self.assertEqual(T["bar"], 2)
        self.assertEqual(T["baz"], 3)
        self.assertRaises(KeyError, T.__getitem__, "ba")
        self.assertRaises(KeyError, T.__getitem__, "fool")
        del T["bar"]
        self.assertRaises(KeyError, T.__getitem__, "bar")
        self.assertEqual(T["baz"], 3)

    def testEmptyStringKey(self) -> None:
        T = Trie(2, foo=1)
        self.assertTrue("foo" in T)
        self.assertTrue("" in T)
        del T[""]
        self.assertRaises(KeyError, T.__getitem__, "")

    def testIterator(self) -> None:
        T = Trie(ba=2, baz=3, fool=1)
        self.assertListEqual(sorted(["fool", "ba", "baz"]), sorted(list(T)))
        T[""] = 0
        self.assertEqual(sorted(["", "fool", "ba", "baz"]), sorted(list(T)))

    def testSingleEntry(self) -> None:
        T = Trie(foo=5)
        self.assertListEqual(["foo"], list(T.keys()))
        self.assertListEqual([5], list(T.values()))
        self.assertListEqual([("foo", 5)], list(T.items()))

    def testValues(self) -> None:
        T = Trie()
        T["ba"] = 2
        # FIXME: Trie allows int as value currently.
        # T["baz"] = "hey's"
        # T["fool"] = 1.5
        T["baz"] = 3
        T["fool"] = 1
        self.assertListEqual(
            sorted(["2", "3", "1"]), sorted([str(v) for v in T.values()])
            # FIXME: Trie allows int as value currently.
            # sorted(["2", "hey's", "1.5"]), sorted([str(v) for v in T.values()])
        )

    def testStrRepr(self) -> None:
        T = Trie()
        T["ba"] = 2
        # FIXME: Trie allows int as value currently.
        # T["baz"] = "hey's"
        # T["fool"] = 1.5
        T["baz"] = 3
        T["fool"] = 1
        result = repr(T)
        self.assertTrue(result.startswith("Trie({"), result)
        self.assertTrue(result.endswith("})"), result)
        self.assertTrue("'ba': 2" in result, result)
        # FIXME: Trie allows int as value currently.
        # self.assertTrue("'baz': \"hey's\"" in result, result)
        # self.assertTrue("'fool': 1.5" in result, result)
        self.assertTrue("'baz': 3" in result, result)
        self.assertTrue("'fool': 1" in result, result)

    def testGetItems(self) -> None:
        T = Trie()
        T["ba"] = 2
        T["baz"] = 3
        T["fool"] = 1
        self.assertEqual(("ba", 2), T.item("bar"))
        self.assertEqual(1, T.value("fool"))
        self.assertRaises(KeyError, T.key, "foo")
        T[""] = 0
        self.assertEqual(("", 0), T.item(""))
        self.assertEqual("", T.key("foo"))

    def testGetExactMatch(self) -> None:
        T = Trie(exact=5)
        # FIXME: The signature is incompatible with Mapping.
        # self.assertListEqual(["exact"], list(T.keys("exact")))
        self.assertListEqual([5], list(T.values("exact")))
        self.assertListEqual([("exact", 5)], list(T.items("exact")))

    def testFakeDefault(self) -> None:
        T = Trie()
        fake = _NonTerminal()
        self.assertEqual(fake, T.value("foo", default=fake))

    def testIterItems(self) -> None:
        T = Trie(ba=2, baz=3, fool=1)
        # FIXME: The signature is incompatible with Mapping.
        # self.assertListEqual(["ba", "baz"], list(T.keys("bazar")))
        self.assertListEqual([("fool", 1)], list(T.items("fools")))
        self.assertListEqual([], list(T.values("others")))

    def testIsPrefix(self) -> None:
        T = Trie(bar=2, baz=3, fool=1)
        self.assertTrue(T.is_prefix("ba"))
        self.assertFalse(T.is_prefix("fools"))
        self.assertTrue(T.is_prefix(""))

    def testIterPrefix(self) -> None:
        T = Trie()
        T["b"] = 1
        T["baar"] = 2
        T["baahus"] = 3
        self.assertListEqual(sorted(["baar", "baahus"]), sorted(list(T.iter("ba"))))
        self.assertListEqual(sorted(["baar", "baahus"]), sorted(list(T.iter("baa"))))
        self.assertListEqual(sorted(["b", "baar", "baahus"]), sorted(list(T.iter("b"))))
        self.assertListEqual(sorted([]), sorted(list(T.iter("others"))))

    def testOffsetMatching(self) -> None:
        T = Trie()
        T["foo"] = 1
        T["baar"] = 2
        T["baarhus"] = 3
        T["bazar"] = 4
        txt = "The fool baal baarhus in the bazar!"
        # FIXME: The signature is incompatible with Mapping.
        # keys = []
        values = []
        items = []
        for i in range(len(txt)):
            values.extend(T.values(txt, i))
        # FIXME: The signature is incompatible with Mapping.
        # for i in range(len(txt)):
        #     keys.extend(T.keys(txt, i))
        for i in range(len(txt)):
            items.extend(T.items(txt, i))
        self.assertListEqual([1, 2, 3, 4], values)
        # FIXME: The signature is incompatible with Mapping.
        # self.assertListEqual(["foo", "baar", "baarhus", "bazar"], keys)
        self.assertListEqual(
            [("foo", 1), ("baar", 2), ("baarhus", 3), ("bazar", 4)], items
        )

    # FIXME: Trie allows int as value currently.
    # def testKeyPresenceOnly(self) -> None:
    #     T = Trie(foo=True, baar=True, baarhus=True, bazar=True)
    #     txt = "The fool baal baarhus in the bazar!"
    #     presence = [4, 14, 29]
    #     for i in range(len(txt)):
    #         if T.value(txt, i, default=False):
    #             self.assertTrue(
    #                 i in presence, '{} {} "{}"'.format(str(presence), i, txt[i:])
    #             )
    #             presence.remove(i)
    #     self.assertEqual(0, len(presence), str(presence))

    def testWindowMatching(self) -> None:
        T = Trie(foo=1, foobar=2)
        # FIXME: The signature is incompatible with Mapping.
        # self.assertListEqual(["foo"], list(T.keys("foobar", 0, 3)))
        self.assertListEqual([1], list(T.values("a foobar!", 2, 7)))
        self.assertListEqual(
            [("foo", 1), ("foobar", 2)], list(T.items("a foobar!", 2, 8))
        )
        self.assertEqual("foo", T.key("foobar", 0, 3))
        self.assertEqual(1, T.value("a foobar!", 2, 7))
        self.assertEqual(("foobar", 2), T.item("a foobar!", 2, 8))

    def testBorderlineValues(self) -> None:
        T = Trie(foo=1, bar=2)
        self.assertEqual("foo", T.key("foo", -3))
        self.assertEqual("foo", T.key("foo", -4))
        self.assertEqual("foo", T.key("foo", -4, 3))
        self.assertEqual(None, T.key("foo", -3, -4, None))
        self.assertEqual(None, T.key("foo", -4, -4, None))


if __name__ == "__main__":
    main()
