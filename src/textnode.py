from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    LINK = 4
    IMAGE = 5
    CODE = 6


class TextNode:
    def __init__(self, text, text_type:TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        if isinstance(value, TextNode):
            return self.text == value.text and self.text_type == value.text_type and self.url == value.url
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value=text_node.text, props={"src": text_node.url, "alt": text_node.text})
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    else:
        raise ValueError(f"Unknown TextType: {text_node.text_type}")
