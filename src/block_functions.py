from markdownnode import BlockType
from converters import TextType, TextNode, text_node_to_html_node, text_to_textnodes
from htmlnode import ParentNode

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]

def block_to_block_type(block):
    # Code block: starts and ends with ```
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Heading: 1–6 '#' followed by a space
    if block.startswith("#"):
        parts = block.split(" ", 1)
        if len(parts) > 1 and 1 <= len(parts[0]) <= 6 and all(c == "#" for c in parts[0]):
            return BlockType.HEADING

    # Quote block: every line starts with '>'
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with '- '
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: starts with increasing numbers '1. ', '2. ', etc.
    if all(line.split(". ", 1)[0].isdigit() for line in lines if ". " in line):
        expected = [f"{i+1}. " for i in range(len(lines))]
        if all(line.startswith(expected[i]) for i, line in enumerate(lines)):
            return BlockType.ORDERED_LIST

    # Otherwise it's a normal paragraph
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    # 1. Split the markdown text into blocks
    blocks = markdown_to_blocks(markdown)

    # 2. Prepare a list to store all block-level HTML nodes
    children = []

    # 3. Loop through each block
    for block in blocks:
        block_type = block_to_block_type(block)

        # 4. Handle each block type
        if block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html_node(block)

        elif block_type == BlockType.HEADING:
            node = heading_to_html_node(block)

        elif block_type == BlockType.CODE:
            node = code_to_html_node(block)

        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)

        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_to_html_node(block)

        elif block_type == BlockType.ORDERED_LIST:
            node = ordered_list_to_html_node(block)

        else:
            raise Exception(f"Unknown block type: {block_type}")

        # 5. Add to parent children
        children.append(node)

    # 6. Return a parent div node that contains all block nodes
    return ParentNode("div", children)

def paragraph_to_html_node(block):
    children = text_to_children(block)
    return ParentNode("p", children)

def heading_to_html_node(block):
    # count the number of # at the start
    level = len(block.split(" ")[0])
    text = block[level+1:] if block[level] == ' ' else block[level:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    # remove triple backticks
    code_text = block.strip("`").strip()
    text_node = TextNode(code_text, TextType.TEXT)
    code_child = text_node_to_html_node(text_node)
    return ParentNode("pre", [ParentNode("code", [code_child])])

def quote_to_html_node(block):
    # remove '> ' from each line
    lines = [line.lstrip('> ').strip() for line in block.split('\n')]
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    lines = [line.lstrip('-* ').strip() for line in block.split('\n')]
    li_nodes = [ParentNode("li", text_to_children(line)) for line in lines]
    return ParentNode("ul", li_nodes)

def ordered_list_to_html_node(block):
    lines = [line.lstrip('0123456789. ').strip() for line in block.split('\n')]
    li_nodes = [ParentNode("li", text_to_children(line)) for line in lines]
    return ParentNode("ol", li_nodes)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]