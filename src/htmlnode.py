
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self): 
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None:
            return ""
        else:
            formatted = []
            for key, value in self.props.items():
                formatted.append(f'{key}="{value}"')
            return " " + " ".join(formatted)
        
    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"

"""
    Add a to_html(self) method. For now, it should just raise a NotImplementedError. 
        Child classes will override this method to render themselves as HTML.
    Add a props_to_html(self) method. 
        It should return a string that represents the HTML attributes of the node. 
        For example, if self.props is:

{
    "href": "https://www.google.com",
    "target": "_blank",
}

Then self.props_to_html() should return:

 href="https://www.google.com" target="_blank"

Notice the leading space character before href and before target. This is important. HTML attributes are always separated by spaces.
    Add a __repr__(self) method. Give yourself a way to print an HTMLNode object and see its tag, value, children, and props. This will be useful for your debugging.
    Create some tests for the HTMLNode class (at least 3). I used a new file called src/test_htmlnode.py. Create a few nodes and make sure the props_to_html method works as expected.
    When you're satisfied that your class is behaving as expected and your unit tests are running successfully, run and submit the tests.

"""