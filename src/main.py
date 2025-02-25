from textnode import TextNode, TextType

def main():
    # Create a test node with some sample values
    node = TextNode("this is node", TextType.BOLD_TEXT, None)
    print(node)

if __name__ == "__main__":
    main()