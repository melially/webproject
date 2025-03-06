from enum import Enum
from htmlnode import HTMLNode, text_node_to_html_node
from delimiter import text_to_textnodes

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

def text_to_children(text):
    # Convert text to TextNode(s)
    text_nodes = text_to_textnodes(text)
    # Convert each TextNode to an HTMLNode
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        # Debug: print what's happening
        print(f"Block: {block[:20]}...")  # Print first 20 chars
        print(f"Type: {block_type}")
        
        if block_type == BlockType.PARAGRAPH:
            html_nodes.append(parse_paragraph(block))
        elif block_type == BlockType.HEADING:
            html_nodes.append(parse_heading(block))
        elif block_type == BlockType.CODE:
            html_nodes.append(parse_code_block(block))
        elif block_type == BlockType.QUOTE:
            html_nodes.append(parse_quote_block(block))
        elif block_type == BlockType.UNORDERED_LIST:
            html_nodes.append(parse_unord_list_block(block))
        elif block_type == BlockType.ORDERED_LIST:
            html_nodes.append(parse_ord_list_block(block))
    
    # Debug: print how many nodes were created
    print(f"Created {len(html_nodes)} HTML nodes")
    
    # Create a div as the parent node
    parent_node = HTMLNode("div", None, html_nodes, None)  # Make sure html_nodes is
    return parent_node
'''
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == "PARAGRAPH":
            html_nodes.append(parse_paragraph(block))
        elif block_type == "HEADING":
            html_nodes.append(parse_heading(block))
        elif block_type == "CODE":
            html_nodes.append(parse_code_block(block))
        elif block_type == "QUOTE":
            html_nodes.append(parse_quote_block(block))
        elif block_type == "UNORDERED_LIST":
            html_nodes.append(parse_unord_list_block(block))
        elif block_type == "ORDERED_LIST":
            html_nodes.append(parse_ord_list_block(block))
    parent_node = HTMLNode("div", None, None, html_nodes)
    return parent_node
'''
'''
def block_to_html_node(block):
    if block_type == "paragraph":
        # Process inline markdown to create child nodes
        children = text_to_children(block)
        # Create paragraph node with those children
        paragraph_node = HTMLNode("p", None, None, children)
        html_nodes.append(paragraph_node)
    elif block_type == "heading":
        # Similar process for headings
        # ...
    # Handle other block types...
'''
def parse_paragraph(block):
    # Replace newlines with spaces and normalize multiple spaces to a single space
    block = ' '.join(block.strip().split())
    children = text_to_children(block)
    return HTMLNode("p", None, children, None)

def parse_heading(block):
    # Figure out heading level (h1, h2, etc.)
    level = block.count('#')
    # Remove the heading markers and whitespace
    content = block[level:].strip()
    children = text_to_children(content)
    return HTMLNode(f"h{level}", None, children, None)
'''
def parse_code_block(block):
    # Remove the ``` at start and end, but keep interior exactly as is
    # Be careful about leading/trailing spaces
    #lines = block.split('\n')
    # Remove first and last line (the ```)
    #content = '\n'.join(lines[1:-1])
    # Code blocks should NOT process inline markdown
    # Remove the triple backticks
    content = block.strip('`').strip()
    # Create code node without processing inline markdown
    code_node = HTMLNode("code", content, None, None)
    return HTMLNode("pre", None, [code_node], None)
'''
def parse_code_block(block):
    # Split the block into lines and remove backticks
    lines = block.strip().split('\n')
    
    # Find start and end of code content (skip the ``` lines)
    start = 0
    end = len(lines)
    for i, line in enumerate(lines):
        if line.strip() == '```':
            if start == 0:
                start = i + 1
            else:
                end = i
                break
    
    # Extract the code content
    code_lines = lines[start:end]
    
    # Remove common indentation if present
    if code_lines:
        non_empty_lines = [line for line in code_lines if line.strip()]
        if non_empty_lines:
            min_indent = min(len(line) - len(line.lstrip()) for line in non_empty_lines)
            code_lines = [line[min_indent:] if len(line) >= min_indent else line for line in code_lines]
    
    # Join with newlines and ensure it ends with a newline
    content = '\n'.join(code_lines)
    if not content.endswith('\n'):
        content += '\n'
    
    # Create the HTML nodes
    code_node = HTMLNode("code", content, None, None)
    pre_node = HTMLNode("pre", None, [code_node], None)
    
    return pre_node

def parse_quote_block(block):
    # Remove the '> ' from the beginning of each line
    content = block.replace('> ', '').strip()    
    children = text_to_children(content)
    return HTMLNode("blockquote", None, children, None)


def parse_unord_list_block(block):
    # Split the block into individual list items
    items = block.split('\n')
    list_item_nodes = []
    
    for item in items:
        # Remove the '- ' from the beginning
        if item.strip().startswith('- '):
            item_content = item.strip()[2:]
            # Process inline markdown in the list item
            item_children = text_to_children(item_content)
            # Create li node for this item
            li_node = HTMLNode("li", None, None, item_children)
            list_item_nodes.append(li_node)
    
    # Create the ul container with all list items
    return HTMLNode("ul", None, list_item_nodes, None)
 
def parse_ord_list_block(block):
    # Split the block into individual list items
    items = block.split('\n')
    list_item_nodes = []
    
    for item in items:
        # Strip leading whitespace and check if it looks like an ordered list item
        stripped_item = item.strip()
        if stripped_item and stripped_item[0].isdigit():
            # Find the position after the number and dot
            dot_pos = stripped_item.find('. ')
            if dot_pos != -1:
                # Extract content after the number and dot
                item_content = stripped_item[dot_pos + 2:]
                # Process inline markdown in the list item
                item_children = text_to_children(item_content)
                # Create li node for this item
                li_node = HTMLNode("li", None, None, item_children)
                list_item_nodes.append(li_node)
    # Create the ol container with all list items
    return HTMLNode("ol", None, list_item_nodes, None)
'''
Let's refine your approach:

    Split the markdown into blocks (which you're already doing)
    Create an empty list to store HTML nodes
    Loop through each block:
        Determine the block type (which you're already doing)
        Create an appropriate HTML node based on that type
        Add that node to your list
    Create a parent div node
    Add all the nodes from your list as children to the parent node
    Return the parent node
'''
'''
Create a new function called def markdown_to_html_node(markdown): that converts a 
    full markdown document into a single parent HTMLNode. That one parent HTMLNode 
    should (obviously) contain many child HTMLNode objects representing the nested elements.

FYI: I created an additional 8 helper functions to keep my code neat and easy to understand, because there's a lot of logic necessary for markdown_to_html_node. I don't want to give you my exact functions because I want you to do this from scratch. However, I'll give you the basic order of operations:

    Split the markdown into blocks (you already have a function for this)
    Loop over each block:
        Determine the type of block (you already have a function for this)
        Based on the type of block, create a new HTMLNode with the proper data
        Assign the proper child HTMLNode objects to the block node. I created a 
            shared text_to_children(text) function that works for all block types. 
            It takes a string of text and returns a list of HTMLNodes that represent 
            the inline markdown using previously created functions (think TextNode -> HTMLNode).
        The "code" block is a bit of a special case: it should not do any inline 
            markdown parsing of its children. I didn't use my text_to_children function 
            for this block type, I manually made a TextNode and used text_node_to_html_node.
    Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.
'''