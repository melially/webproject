from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        #parsed_nodes = []

        while True:
            # Start and End indexes of delimiters
            start_index = remaining_text.find(delimiter)

            if start_index == -1: # No delimiters, break
                new_nodes.append(TextNode(remaining_text, TextType.NORMAL_TEXT))  # Add the rest as plain text
                break
    
            end_index = remaining_text.find(delimiter, start_index + len(delimiter)) # A string to parse for the closing delimiter
            if end_index == -1 : # Signals a lack of closing delimiter
                raise Exception ("Missing closing delimiter")

            # Cut into segments
            prior_text = remaining_text[:start_index]
            alt_text = remaining_text[start_index + len(delimiter):end_index]
            remaining_text = remaining_text[end_index + len(delimiter):]

            # Assign proper TextType to each
            if prior_text: # Adds only if there's already text
                new_nodes.append(TextNode(prior_text, TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(alt_text, text_type))  # The special formatted segment

    return new_nodes

def process_all_delimiters(nodes):
    # Process bold markers
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    # Process italic markers
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    # Process code markers
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    # Return fully processed nodes
    return nodes

def extract_markdown_images(text):

    # Raw markdown to a list of tuples w/ (alt-text, url)
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    # Raw markdown to a list of tuples w/ (anchor text, url)
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
            continue
        
        # image_nodes = extract_markdown_images(old_nodes) <- Wrong, needs to be on the text, not list of nodes
        image_tuples = extract_markdown_images(node.text)
        
        # If no images, just add the original node and continue
        if not image_tuples:
            new_nodes.append(node)
            continue
        
        remaining_text = node.text
        
        for image_alt, image_url in image_tuples:
            image_markdown = f"![{image_alt}]({image_url})"
            parts = remaining_text.split(image_markdown, 1)

            # Add text before image if not empty
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL_TEXT))
                
            # Add the image node
            new_nodes.append(TextNode(image_alt, TextType.IMAGE_TEXT, image_url))
            
            # Update remaining text
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
                
        # Add any remaining text after the last image
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL_TEXT))

    return new_nodes      

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
            continue

        link_tuples = extract_markdown_links(node.text)
        
        # If no links, just add the original node and continue
        if not link_tuples:
            new_nodes.append(node)
            continue
        
        remaining_text = node.text
        
        for anchor_text, url in link_tuples:
            link_markdown = f"[{anchor_text}]({url})"
            parts = remaining_text.split(link_markdown, 1)

            # Add text before link if not empty
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL_TEXT))
                
            # Add the link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK_TEXT, url))
            
            # Update remaining text
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
                
        # Add any remaining text after the last link
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL_TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL_TEXT)]
    nodes = process_all_delimiters(nodes)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

    '''
    This is **text** with an _italic_ word and a 
        `code block` and an ![obi wan image]
        (https://i.imgur.com/fJRm4Vk.jpeg) and a 
        [link](https://boot.dev)
    '''

    #becomes

    '''
    [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
]
    '''