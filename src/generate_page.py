def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# "):  # single # only
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")