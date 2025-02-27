import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_htmlnode(self):
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        print(node.props_to_html())
        # Should output: ' href="https://google.com" target="_blank"'
        
        node = HTMLNode(props={"href": "https://bing.com", "target": "Who CARES"})
        print(node.props_to_html())

        node = HTMLNode(props={"href": "dummy", "tget": "Sbank"})
        print(node.props_to_html())

    def test_leaf_to_html_p(self): # Test a basic paragraph tag
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_with_props(self):  # Test a tag with properties
        node = LeafNode("a", "Click me!", {"href": "https://www.example.com", "class": "button"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com" class="button">Click me!</a>')
    # Note: dictionary order isn't guaranteed, so if the test fails, the properties might be in a different order

    def test_leaf_no_tag(self): # Test a leaf with no tag (just raw text)
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_missing_value(self): # Test that a ValueError is raised when value is None
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_special_characters(self): # Test HTML with special characters
        node = LeafNode("div", "This has <b>bold</b> text & symbols")
        self.assertEqual(node.to_html(), "<div>This has <b>bold</b> text & symbols</div>")

    def test_leaf_empty_string_value(self): # Test an empty string is a valid value
        node = LeafNode("span", "")
        self.assertEqual(node.to_html(), "<span></span>")
    
    def test_leaf_with_numeric_value(self): # Test that numeric values are converted to strings
        node = LeafNode("span", 42)
        self.assertEqual(node.to_html(), "<span>42</span>")

    def test_leaf_with_boolean_prop(self): # Test boolean properties
        node = LeafNode("button", "Submit", {"disabled": True})
        self.assertEqual(node.to_html(), '<button disabled="True">Submit</button>')

    def test_leaf_with_multiple_props(self): # Test many properties
        node = LeafNode("input", "", {
            "type": "text",
            "name": "username",
            "placeholder": "Enter username",
            "required": True,
            "maxlength": 50
        }) # The exact string might vary due to dict order, but should contain all properties
        html = node.to_html()
        self.assertIn('<input', html)
        self.assertIn('type="text"', html)
        self.assertIn('name="username"', html)
        self.assertIn('placeholder="Enter username"', html)
        self.assertIn('required="True"', html)
        self.assertIn('maxlength="50"', html)
        self.assertIn('></input>', html)

    def test_leaf_constructor_rejects_children(self):
        # Test that providing children to a LeafNode raises an error or is ignored
        # This depends on how your HTMLNode parent class is implemented
        # If it silently ignores children, test that they're not included
        # If it raises an error, test for that
        node = LeafNode("p", "Text", {}, ["child1", "child2"])
        self.assertEqual(node.children, None)  # or however you're storing children

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    # Should have more tests for parentnode

if __name__ == "__main__":
    unittest.main()