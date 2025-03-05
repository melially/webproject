import unittest
from enum import Enum
from blockhandling import markdown_to_blocks, block_to_block_type, BlockType
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


if __name__ == "__main__":
    unittest.main()