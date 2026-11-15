from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        if not self.children:
            raise ValueError("All parent nodes must have children")
        props_string = self.props_to_html()
        children_string = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_string}>{children_string}</{self.tag}>"