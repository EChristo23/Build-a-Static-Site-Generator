from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value
        props_string = self.props_to_html()
        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
    