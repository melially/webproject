import unittest

from textnode import TextNode, TextType
from delimiter import split_nodes_delimiter, process_all_delimiters, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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

class TestDelimiterOnTextNode(unittest.TestCase):
    
    def test_bold_text(self):
        nodes = [TextNode("I am **bold** text!", TextType.NORMAL_TEXT)]
        result = process_all_delimiters(nodes)
        
        # Expected result after processing bold text
        expected = [
            TextNode("I am ", TextType.NORMAL_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" text!", TextType.NORMAL_TEXT)
        ]
        
        self.assertEqual(result, expected)

    def test_italic_text(self):
        nodes = [TextNode("This _italic_ portion.", TextType.NORMAL_TEXT)]
        result = process_all_delimiters(nodes)

        # Expected result after processing italic text
        expected = [
            TextNode("This ", TextType.NORMAL_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" portion.", TextType.NORMAL_TEXT)
        ]

        self.assertEqual(result, expected)

    def test_multiple_bold(self):
        nodes = [TextNode("Multiple **bold** and **strong** text.", TextType.NORMAL_TEXT)]
        result = process_all_delimiters(nodes)

        # Expected result after processing bold text
        expected = [
            TextNode("Multiple ", TextType.NORMAL_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" and ", TextType.NORMAL_TEXT),
            TextNode("strong", TextType.BOLD_TEXT),
            TextNode(" text.", TextType.NORMAL_TEXT)
        ]

        self.assertEqual(result, expected)

    #Need more tests below
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches) 

    # Need more tests for images and links
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGE_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode(
                    "second image", TextType.IMAGE_TEXT, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [linky loo](https://i.imgur.com/zjjcJKZ.png) and another [linked image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("linky loo", TextType.LINK_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode(
                    "linked image", TextType.LINK_TEXT, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        node = TextNode(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = text_to_textnodes(node.text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL_TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word and a ", TextType.NORMAL_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" and an ", TextType.NORMAL_TEXT),
                TextNode("obi wan image", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL_TEXT),
                TextNode("link", TextType.LINK_TEXT, "https://boot.dev"),
            ],
            new_nodes
        )


if __name__ == "__main__":
    unittest.main()