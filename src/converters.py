from textnode import TextNode, TextType
from htmlnode import LeafNode
import re

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    elif text_node.text_type == TextType.LINK:
        if not text_node.url:
            raise ValueError("Link TextNode must have a URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})

    elif text_node.text_type == TextType.IMAGE:
        if not text_node.url:
            raise ValueError("Image TextNode must have a src URL")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    else:
        raise Exception(f"Unknown TextType: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # Only split text nodes, ignore others
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        # If no delimiter is found, keep it as-is
        if len(parts) == 1:
            new_nodes.append(node)
            continue

        # If odd number of delimiters — invalid format
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid delimiter count in: {node.text}")

        # Alternate between TEXT and given text_type
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

"""def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes"""

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # Skip non-text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_images(text)

        if not matches:
            new_nodes.append(node)
            continue

        for alt_text, url in matches:
            # Find the markdown pattern for this image
            pattern = f"![{alt_text}]({url})"
            parts = text.split(pattern, 1)

            # Add text before image
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            # Continue with remaining text
            text = parts[1]

        # Add leftover text after last image
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # Skip non-text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_links(text)

        if not matches:
            new_nodes.append(node)
            continue

        for anchor_text, url in matches:
            # Find the markdown pattern for this link
            pattern = f"[{anchor_text}]({url})"
            parts = text.split(pattern, 1)

            # Add text before link
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))

            # Continue with remaining text
            text = parts[1]

        # Add leftover text after last link
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes,"**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,"_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,"`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes