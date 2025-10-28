import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from converters import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link,text_to_textnodes
from textnode import TextNode, TextType
from block_functions import markdown_to_blocks

class TestHTMLNode(unittest.TestCase):
    """def test_parent_to_html_basic(self):
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

    def test_split_nodes_code(self):
        node = TextNode("This is `code` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(result) == 3
        assert result[0].text == "This is "
        assert result[1].text == "code"
        assert result[1].text_type == TextType.CODE
        assert result[2].text == " here"


    def test_split_nodes_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(result) == 3
        assert result[1].text_type == TextType.BOLD


    def test_split_nodes_multiple_formats(self):
        node = TextNode("Mix of `code` and **bold**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert any(n.text_type == TextType.CODE for n in nodes)
        assert any(n.text_type == TextType.BOLD for n in nodes)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
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
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_text_node(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(node)
        self.assertEqual(new_nodes, [
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
        ])

    def test_basic_markdown(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
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
            ],
        )

    def test_no_formatting(self):
        text = "Just plain text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, [TextNode("Just plain text", TextType.TEXT)])

    def test_only_bold(self):
        text = "This is **bold**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_mixed_formatting_order(self):
        text = "_italic_ and **bold** and `code`"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )"""
        
if __name__ == "__main__":
    unittest.main()