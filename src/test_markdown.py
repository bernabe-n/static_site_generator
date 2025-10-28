import unittest
from block_functions import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
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

    def test_markdown_to_blocks_newlines(self):
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

    def test_heading_block(self):
        assert block_to_block_type("# Hello") == BlockType.HEADING
        assert block_to_block_type("###### Tiny") == BlockType.HEADING

    def test_code_block(self):
        block = "```\nprint('Hello')\n```"
        assert block_to_block_type(block) == BlockType.CODE

    def test_quote_block(self):
        block = "> quote line 1\n> quote line 2"
        assert block_to_block_type(block) == BlockType.QUOTE

    def test_unordered_list_block(self):
        block = "- item 1\n- item 2"
        assert block_to_block_type(block) == BlockType.UNORDERED_LIST

    def test_ordered_list_block(self):
        block = "1. first\n2. second\n3. third"
        assert block_to_block_type(block) == BlockType.ORDERED_LIST

    def test_paragraph_block(self):
        block = "Just a simple paragraph of text."
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_markdown_to_html_node_paragraph(self):
        md = "This is **bold** and _italic_ text."
        node = markdown_to_html_node(md)
        html = node.to_html()
        assert html == '<div><p>This is <b>bold</b> and <i>italic</i> text.</p></div>'


    def test_markdown_to_html_node_code_block(self):
        md = "```\nprint('Hello')\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        assert html == "<div><pre><code>print('Hello')</code></pre></div>"


if __name__ == "__main__":
    unittest.main()