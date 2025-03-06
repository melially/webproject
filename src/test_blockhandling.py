import unittest
from enum import Enum
from blockhandling import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
#MORE TEST PLZ>>>>>>
def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )

class TestBlockTypeFunction(unittest.TestCase):
    
    def test_heading(self):
        # Test for headings with different levels
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        
        # Test that 7 # characters isn't a heading
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)
        
        # Test that # without space isn't a heading
        self.assertEqual(block_to_block_type("#Not a heading"), BlockType.PARAGRAPH)
    
    def test_code(self):
        # Test basic code block
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)
        
        # Test code block with language specifier
        self.assertEqual(block_to_block_type("```python\ndef hello():\n    print('hello')\n```"), BlockType.CODE)
        
        # Test that incomplete code markers aren't code blocks
        self.assertEqual(block_to_block_type("``\nNot a code block\n``"), BlockType.PARAGRAPH)
    #MORE TESTS DAMMIT
    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()