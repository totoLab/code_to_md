#!/usr/bin/python3

import sys, os, re, subprocess

def log_err(msg):
    print(f"ERR: {msg}")
    sys.exit(1)

def check_ext(file, ext_filter):
    return len(ext_filter) == 0 or any(file.endswith(ext) for ext in ext_filter)

def append_to_code_block(title, code, ext):
    return f"### {title} \n```{ext} \n{code}\n```\n"

def main(rootdir, ext_filter, output_filename):
    file_content = ""
    for subdir, dirs, files in os.walk(rootdir):
        dirs.sort()
        file_content += f"## {subdir.split('/')[-1]} \n"
        for file in files:
            filename, ext = file.split(".")
            full_path = os.path.join(subdir, file)
            if check_ext(file, ext_filter):
                block = ""
                with open(full_path, "r") as f:
                    block = append_to_code_block(filename, f.read(), ext)

                file_content += block + "\n"

    md_filename = f"{output_filename}.md"
    try:
        with open(md_filename, "w") as f:
            f.write(file_content)
            print(f"File saved as {md_filename}")
    except e:
        print(f"Error while generating {md_filename}")
        sys.exit(1)

    generate_pdf = input(f"Want to generate pdf from {md_filename}? [y/N] ")
    if re.match("y|Y", generate_pdf):
        try:
            subprocess.call(["md-to-pdf", md_filename], stderr=subprocess.DEVNULL)
            print(f"File saved as {output_filename}.pdf")
        except subprocess.CalledProcessError as e:
            print(f"Conversion failed with error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        log_err(f"not enough args {args}")
    dir = args[1]
    
    extensions = []
    if len(args) > 2:
        filter = args[2]
        extensions = filter.split(",")

    if os.path.isdir(dir) and os.path.exists(dir):
        main(os.path.abspath(dir), extensions, "out")
