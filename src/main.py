import os
from textnode import TextNode, TextType
import os
import shutil
from copystatic import copy_files_recursive
from generate_page import generate_page


#dir_path_static = "./static"
#dir_path_public = "./public"
def generate_site(content_dir, template_path, public_dir):
    for root, dirs, files in os.walk(content_dir):
        for filename in files:
            if filename.endswith(".md"):
                from_path = os.path.join(root, filename)
                rel_path = os.path.relpath(from_path, content_dir)
                dest_path = os.path.join(public_dir, rel_path)
                dest_path = dest_path.replace(".md", ".html")

                print(f"Generating page from {from_path} to {dest_path} using {template_path}")
                generate_page(from_path, template_path, dest_path)

def main():
    """print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)"""
    # 1. Delete `public` if it exists
    if os.path.exists("public"):
        shutil.rmtree("public")

    # 2. Copy `static` to `public`
    shutil.copytree("static", "public", dirs_exist_ok=True)

    # 3. Generate main page
    generate_site("content", "template.html", "public")
    #generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()