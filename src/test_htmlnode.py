import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from converters import text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_parent_to_html_basic(self):
        child = LeafNode("b", "Bold text")
        parent = ParentNode("p", [child])
        expected = "<p><b>Bold text</b></p>"
        self.assertEqual(parent.to_html(), expected)

    def test_parent_to_html_nested(self):
        bold = LeafNode("b", "bold")
        italic = LeafNode("i", "italic")
        parent = ParentNode("p", [bold, italic])
        expected = "<p><b>bold</b><i>italic</i></p>"
        self.assertEqual(parent.to_html(), expected)

    def test_parent_with_props(self):
        child = LeafNode("span", "Text")
        parent = ParentNode("div", [child], {"class": "container"})
        expected = '<div class="container"><span>Text</span></div>'
        self.assertEqual(parent.to_html(), expected)

    def test_missing_tag_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "test")])

    def test_missing_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")

    def test_link(self):
        node = TextNode("Google", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/image.png", "alt": "Alt text"}
        )

    def test_invalid_type(self):
        class FakeType:
            pass
        node = TextNode("Unknown", FakeType())
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()