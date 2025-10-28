import os
from block_functions import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# "):  # single # only
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read files
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown)
    content_html = html_node.to_html()

    # Extract title
    title = extract_title(markdown)

    # Replace placeholders
    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", content_html)

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write final HTML
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)
