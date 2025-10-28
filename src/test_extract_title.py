from src.generate_page import extract_title

def test_extract_title_basic():
    assert extract_title("# Hello World") == "Hello World"

def test_extract_title_with_whitespace():
    assert extract_title("   #  My Title  ") == "My Title"