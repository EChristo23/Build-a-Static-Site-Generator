import re
from enum import Enum

from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

_map = {
    'PARAGRAPH': 'p',
    'HEADING': 'h',
    'CODE': 'code',
    'QUOTE': 'q',
    'OLIST': 'p',
    'ULIST': 'p',
}

def markdown_to_blocks(markdown):

    blocks = re.split("\n\\s*\n", markdown) # markdown.split("\n\n")
    blocks = [i.strip() for i in blocks if i != ""]
    return blocks


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    # Heading 
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # Code
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    # Paragraph
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    # Unordered List
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    # Ordered List
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def heading_to_html(heading:str):
    pass

def to_html_node(block, type: BlockType):
    '''Take one Markdown block and its type and return the corresponding block-level HTMLNode.'''
    if type == BlockType.PARAGRAPH:        
        text_nodes = text_to_textnodes(block.replace('\n', ' '))
        html_nodes = [text_node_to_html_node(t) for t in text_nodes]
        node = ParentNode(
            tag='p',
            children=html_nodes
        )
        return node

    if type == BlockType.HEADING:
        # Get headign
        header = re.search(r"#.*", block).group()
        # Get "#" count
        header_string = re.search(r"#*\s", header).group().strip()
        count = len(header_string)
        # Create header nodes
        header_text = re.split(r"#+\s", header, 1)[-1].strip()
        header_text_node = text_to_textnodes(header_text)
        header_html_nodes = [text_node_to_html_node(t) for t in header_text_node]

        # Remaining Text
        remain = block.split(header, 1)[-1]
        remaining_nodes = text_to_textnodes(remain)
        text_nodes_html = [text_node_to_html_node(t) for t in remaining_nodes]

        # Combine nodes
        children = header_html_nodes

        children.extend(text_nodes_html)

        node = ParentNode(
                    tag=f'h{count}',
                    children=children
                )
        return node

    if type == BlockType.CODE:
        code_nodes = TextNode(re.search(r"```\n(.*?)```", block, re.DOTALL).group(1), TextType.CODE)
        code_html_node = text_node_to_html_node(code_nodes)
        node = ParentNode(
            tag='pre',
            children=[code_html_node]
        )
        return node
    
    if type == BlockType.QUOTE:
        quote_text = re.sub(r'>+\s', '', block).replace('\n', ' ').strip()
        quote_text_nodes = text_to_textnodes(quote_text)
        quote_html_nodes = [text_node_to_html_node(q) for q in quote_text_nodes]
        node = ParentNode(
            tag = 'blockquote',
            children=quote_html_nodes
        )
        return node
    

    if type == BlockType.OLIST:
        olist_text = re.split(r'\n', block)
        items = [re.sub(r'^\d+\.\s', '', i, 1) for i in olist_text]
        items_text_node = [text_to_textnodes(i) for i in items]
        li_nodes_list = []
        for l in items_text_node:
            child_list = []
            for text_node in l:
                html_node = text_node_to_html_node(text_node)
                child_list.append(html_node)
            li_node = ParentNode(
                tag = 'li',
                children = child_list
            )
            li_nodes_list.append(li_node)

        node = ParentNode(
            tag = 'ol',
            children=li_nodes_list
        )
        return node

    if type == BlockType.ULIST:
        ulist_text = re.split(r'\n', block)
        items = [re.sub(r'^-\s', '', i, 1) for i in ulist_text]
        items_text_node = [text_to_textnodes(i) for i in items]
        li_nodes_list = []
        for l in items_text_node:
            child_list = []
            for text_node in l:
                html_node = text_node_to_html_node(text_node)
                child_list.append(html_node)
            li_node = ParentNode(
                tag = 'li',
                children = child_list
            )
            li_nodes_list.append(li_node)

        node = ParentNode(
            tag = 'ul',
            children=li_nodes_list
        )
        return node

    
    return None



def markdown_to_html_node(markdown):
    nodes = []
    # Get blocks
    blocks = markdown_to_blocks(markdown=markdown)
    # Loop over blocks
    for b in blocks:
        # get block type
        block_type = block_to_block_type(b)
        html_node = to_html_node(b, block_type)  #  Parent node of block
        nodes.append(html_node)
    root_node = ParentNode(
        tag='div',
        children= nodes
        )
    return root_node


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = node.text.split(delimiter)
            if len(parts)%2 ==0:
                raise ValueError(f'Invalid markdown without enclosing {delimiter}')            
            for i, p in enumerate(parts):
                if p != '':
                    if ((i%2) !=0):
                        n = TextNode(text = p, text_type=text_type)
                    else:
                        n = TextNode(p, TextType.TEXT)
                    new_nodes.append(n)
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    #  Zip them into a list of tuples
    names_path = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return names_path


def extract_markdown_links(text):
    # Find all anchor texts
    text_links = list(re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text))
    return text_links

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text = node.text
            parts = extract_markdown_links(text)  # Get all the images and links 
            if parts:
                for t in parts:
                    image_alt, image_link = t
                    sections = text.split(f"[{image_alt}]({image_link})", 1)

                    # Text before the image link
                    if sections[0] != '':
                        new_nodes.append(TextNode(text = sections[0], text_type=TextType.TEXT))

                    # Transformat each image link component into its own node
                    n2 = TextNode(text = image_alt, text_type=TextType.LINK, url=image_link)
                    new_nodes.append(n2)

                    # Update text to text after image link
                    text = sections[-1]

                # Remaining text if any
                if sections[-1] != '':
                    new_nodes.append(TextNode(text = sections[-1], text_type=TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text = node.text
            parts = extract_markdown_images(text)  # Get all the images and links 
            if parts:
                for t in parts:
                    image_alt, image_link = t
                    sections = text.split(f"![{image_alt}]({image_link})", 1)

                    # Text before the image link
                    if sections[0] != '':
                        new_nodes.append(TextNode(text = sections[0], text_type=TextType.TEXT))

                    # Transformat each image link component into its own node
                    n2 = TextNode(text = image_alt, text_type=TextType.IMAGE, url=image_link)
                    new_nodes.append(n2)

                    # Update text to text after image link
                    text = sections[-1]

                # Remaining text if any
                if sections[-1] != '':
                    new_nodes.append(TextNode(text = sections[-1], text_type=TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text)->list[TextNode]:
    node_list = []
    node = TextNode(text=text, text_type=TextType.TEXT)
    # BOLD
    node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
    # ITALIC
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    # LINK 
    node_list = split_nodes_link(node_list)
    # IMAGE 
    node_list = split_nodes_image(node_list)
    # CODE
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    return node_list


def main():
    md = '''
- First item
- Second item
- Third item
- Fourth item
'''
    
    html = markdown_to_html_node(md)
    print(html.to_html())



if __name__ == "__main__":
    main()