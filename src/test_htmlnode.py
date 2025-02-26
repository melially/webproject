import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        print(node.props_to_html())
        # Should output: ' href="https://google.com" target="_blank"'
        
        node = HTMLNode(props={"href": "https://bing.com", "target": "Who CARES"})
        print(node.props_to_html())

        node = HTMLNode(props={"href": "dummy", "tget": "Sbank"})
        print(node.props_to_html())
        

if __name__ == "__main__":
    unittest.main()