from enum import Enum

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []

    for block in blocks:
        if block.strip(): # Only accounts for blocks w/ content
            new_blocks.append(block.strip())
    return new_blocks

class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"

def is_heading(block):
    # Check if it starts with 1-6 # characters followed by a space
    if block.startswith('#'):
        # Count the amount of consecutive # chars
        count = 0
        for char in block:
            if char == '#':
                count += 1
            else:
                break

        # Make sure there's between 1 and 6 # chars and a space after
        if 1<= count <= 6 and block[count:count+1] == ' ':
            return True
    return False

def is_code(block):
    # Check if it starts with ``` and ends with ```
    return block.startswith(("```")) and block.endswith(("```"))

def is_quote(block):
    # Check if every line starts with a >
    lines = block.split('\n')
    return all(line.startswith('>') for line in lines)

def is_unordered_list(block):
    # Check if every line starts with a - character, followed by a space
    lines = block.split('\n')
    return all(line.startswith('- ') for line in lines)

def is_ordered_list(block):
    # Check if every line starts with a number character, followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    lines = block.split('\n')
    if not lines:
        return False
    
    for i, line in enumerate(lines, 1): # i starts at 1
        # Check if lines start w/ "i. "
        expected_prefix = f"{i}. "
        if not line.startswith(expected_prefix):
            return False
    return True

def block_to_block_type(block):

    if is_heading(block):
        return BlockType.HEADING
    elif is_code(block):
        return BlockType.CODE
    elif is_quote(block):
        return BlockType.QUOTE
    elif is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    pass

'''
Create a new function called def markdown_to_html_node(markdown): that converts a 
    full markdown document into a single parent HTMLNode. That one parent HTMLNode 
    should (obviously) contain many child HTMLNode objects representing the nested elements.

FYI: I created an additional 8 helper functions to keep my code neat and easy to understand, because there's a lot of logic necessary for markdown_to_html_node. I don't want to give you my exact functions because I want you to do this from scratch. However, I'll give you the basic order of operations:

    Split the markdown into blocks (you already have a function for this)
    Loop over each block:
        Determine the type of block (you already have a function for this)
        Based on the type of block, create a new HTMLNode with the proper data
        Assign the proper child HTMLNode objects to the block node. I created a shared text_to_children(text) function that works for all block types. It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (think TextNode -> HTMLNode).
        The "code" block is a bit of a special case: it should not do any inline markdown parsing of its children. I didn't use my text_to_children function for this block type, I manually made a TextNode and used text_node_to_html_node.
    Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.
'''

'''
Create a block_to_block_type function that takes a single block of markdown text as input and returns the BlockType representing the type of block it is. You can assume all leading and trailing whitespace was already stripped (we did that in a previous lesson).

1.    Headings start with 1-6 # characters, followed by a space and then the heading text.
2.    Code blocks must start with 3 backticks and end with 3 backticks.
3.    Every line in a quote block must start with a > character.
4.    Every line in an unordered list block must start with a - character, followed by a space.
5.    Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
6.    If none of the above conditions are met, the block is a normal paragraph.
'''
