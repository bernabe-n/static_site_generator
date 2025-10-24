print("hello world")
from textnode import TextNode, TextType

def main():
    textnode = TextNode("This is some anchor text", TextType.links, url="http://example.com")
    print(textnode)

if __name__ == "__main__":
    main()