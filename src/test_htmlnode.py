import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_html_node(self):
        node = HTMLNode("div", "Hello, World!", [], {"class": "container"})
        assert node.tag == "div"
        assert node.value == "Hello, World!"
        assert node.children == []
        assert node.props == {"class": "container"}

    def test_html_node_repr(self):
        node = HTMLNode("div", "Hello, World!", [], {"class": "container"})
        assert repr(node) == "HTMLNode(tag=div, value=Hello, World!, children=[], props={'class': 'container'})"

    def test_html_node_to_html(self):
        node = HTMLNode("div", "Hello, World!", [], {"class": "container"})
        try:
            node.to_html()
        except NotImplementedError:
            pass
        else:
            assert False, "Expected NotImplementedError"

if __name__ == "__main__":
    unittest.main()