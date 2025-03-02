from textnode import TextNode, TextType
from htmlnode import HTMLNode, text_node_to_html_node
from delimiter import split_nodes_delimiter


def main():
    # Create a test node with some sample values
    node = TextNode("this is node", TextType.BOLD_TEXT, None)
    print(node)

if __name__ == "__main__":
    main()