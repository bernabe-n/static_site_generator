import os
import sys
import shutil
from copystatic import copy_files_recursive
from generate_page import generate_pages_recursive

def main():
    # 1️⃣ Basepath from CLI or default "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    if not basepath.endswith("/"):
        basepath += "/"

    # 2️⃣ Folder setup
    static_dir = "static"
    content_dir = "content"
    output_dir = "docs"  # GitHub Pages expects this
    template_path = "template.html"

    # 3️⃣ Clean output directory
    if os.path.exists(output_dir):
        print("🗑️  Deleting old docs directory...")
        shutil.rmtree(output_dir)

    # 4️⃣ Copy static files
    print("📁 Copying static files to docs directory...")
    shutil.copytree(static_dir, output_dir, dirs_exist_ok=True)

    # 5️⃣ Generate pages recursively
    print(f"🛠️  Generating pages with basepath: {basepath}")
    generate_pages_recursive(content_dir, template_path, output_dir, basepath)

    print("✨ Site generation complete! All files are in /docs.")


if __name__ == "__main__":
    main()