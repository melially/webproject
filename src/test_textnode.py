import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

        node = TextNode("HI", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD_TEXT, "www.google.com" )
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, "www.google.com")
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()