from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            return self.value or ""
        
        props_str = ""
        if self.props:
            for attr, value in self.props.items():
                props_str += f' {attr}="{value}"'
        
        if self.children:
            children_html = ""
            for child in self.children:
                children_html += child.to_html()
            return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"
        elif self.value:
            return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{props_str}></{self.tag}>" 

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

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None, children=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        # Use super().__init__ to call the parent constructor with our modified parameters

    def to_html(self):
        if self.value is None: # Check if value is None
            raise ValueError("LeafNode missing a value")

        if self.tag is None:
            return self.value
        
        html = f"<{self.tag}" # Start with the opening tag
    
        if self.props: # Add props if there are any
            for prop, value in self.props.items():
                html += f' {prop}="{value}"'
    
        # Close the opening tag and add the value and closing tag
        html += f">{self.value}</{self.tag}>"
        return html

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None: # Check if value is None
            raise ValueError("ParentNode missing a tag")
        if self.children is None: # Check if value is None
            raise ValueError("ParentNode missing children")
        
        if self.props: # Create opening tag with properties
            props_str = ""
            for prop, value in self.props.items():
                props_str += f' {prop}="{value}"'
            html = f"<{self.tag}{props_str}>"
        else:
            html = f"<{self.tag}>"
    
        for child in self.children: # Recursively add HTML from all children
            html += child.to_html()
    
        html += f"</{self.tag}>" # Add closing tag
        
        return html   
'''
Otherwise, return a string representing the HTML tag of the 
    node and its children. This should be a recursive method 
    (each recursion being called on a nested child node). 
    I iterated over all the children and called to_html on each, 
    concatenating the results and injecting them between the 
    opening and closing tags of the parent.
'''
def text_node_to_html_node(text_node):
    # You'll check text_node.text_type here
    if text_node.text_type == TextType.NORMAL_TEXT:
        return LeafNode(None, text_node.text)
    # For each type, return the appropriate LeafNode
    elif text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode("b", text_node.text)
    # For example, for TextType.BOLD, you'd return a LeafNode with tag "b"
    elif text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE_TEXT:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK_TEXT:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE_TEXT:  
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    # Don't forget to handle the case where the type isn't recognized
    else:
        raise ValueError(f"Invalid TextType: {text_node.text_type}")