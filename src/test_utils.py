import unittest

from block import (
    BlockType,
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    markdown_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    text_to_textnodes,
)
from file_generator import extract_title
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

    def test_bold(self):
        node = TextNode("**This starting text is bold**, isn't it?", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("This starting text is bold", TextType.BOLD))

    def test_bold_with_code_delimiter(self):
        node = TextNode("**This `starting` text is bold**, isn't it?", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("This `starting` text is bold", TextType.BOLD))

    def test_unmatched_delimiter(self):
        node = TextNode("This ` delimiter is unmatched", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], '`', TextType.CODE)

    def test_bold_and_text_nodes(self):
        node1 = TextNode("`This starting text is code`, isn't it?", TextType.TEXT)
        node2 = TextNode("**This starting text is bold**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node1, node2], '`', TextType.CODE)
        self.assertEqual(new_nodes[-1], TextNode("**This starting text is bold**", TextType.BOLD))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev")],
            matches
    )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_start(self):
            node = TextNode(
                "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    #TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                ],
                new_nodes,
            )

    def test_text_to_textnodes(self):
        output = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            output,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_heading(self):
        test_block = '''### This is a Headering level 1'''
        test_type = block_to_block_type(test_block)
        self.assertEqual(
            test_type,
            BlockType.HEADING
        )

    def test_block_heading_level(self):
            test_block = '''### This is a Headering level 3'''
            test_type = block_to_block_type(test_block)
            self.assertEqual(
                test_type,
                BlockType.HEADING
            )
    def test_block_non_heading_level(self):
                test_block = '''############ This is not a HEADING'''
                test_type = block_to_block_type(test_block)
                self.assertEqual(
                    test_type,
                    BlockType.PARAGRAPH
                )
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading_block(self):
        md = """
### This is a heading
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a heading</h3></div>",
        )

    def test_heading_block_with_paragraph(self):
        md = """
### This is a heading
This is not a heading
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a heading\nThis is not a heading</h3></div>",
        )

    def test_ordered_list_block(self):
        md = """
1. First item
2. Second item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li></ol></div>",
        )

    def test_unordered_list_block(self):
        md = """
- First item
- Second item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li></ul></div>",
        )

    def test_quote_block(self):
        md = """
> This is a quote
> spanning two lines
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote spanning two lines</blockquote></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title(self):
        md = """
# Title
## Second Title 
Test EST tes
        """
        title = extract_title(md)
        self.assertEqual(title, "Title")
        
    
if __name__ == "__main__":
    unittest.main()