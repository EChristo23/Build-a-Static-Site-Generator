import os
import pathlib
import re
import shutil

from jinja2 import Template

from block import markdown_to_html_node


def clear_and_copy_files(source:str='static', destination:str ='public'):
    # Check if destionation is a valid directory
    if not os.path.exists(destination):
        raise RuntimeError('Invalid destination path')
    # Remove destination directory
    shutil.rmtree(destination)
    copy_files(source, destination)

def copy_files(source:str, destination: str):
    os.mkdir(destination)
    # Copy files
    for name in os.listdir(source):
        src_path = os.path.join(source, name)
        dst_path = os.path.join(destination, name)
        if os.path.isfile(src_path):
            print(f'Copying file {src_path} to {dst_path}')
            shutil.copy(src_path, dst_path)
        else:
            print(f'Creating directory {dst_path}')
            copy_files(src_path, dst_path)

def extract_title(markdown:str)->str:
    title = re.search(r'#\s+([^\r\n]+)', markdown)
    if not title:
        raise Exception('Title not found')
    title = title.group().replace("# ", "").strip()
    return title

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path, mode='r') as f:
        from_file = f.read()
    with open(template_path, mode='r') as f:
        template_file = f.read()
    html = markdown_to_html_node(from_file).to_html()
    title = extract_title(from_file)
    template = Template(template_file)
    rendered_html = template.render(
        Title=title, 
        Content=html
    )
    root_path = pathlib.Path(dest_path)
    dest_path_updated = pathlib.Path(from_path).parts[1:]
    write_path = root_path.joinpath(pathlib.Path(*dest_path_updated))
    write_path.parent.mkdir(parents=True, exist_ok=True)
    write_path = write_path.with_suffix('.html')
    with open(write_path, mode="w", encoding="utf-8") as f:
        f.write(rendered_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    with os.scandir(dir_path_content) as d:
        for e in d:
            if e.is_file() and e.name.endswith('.md'):
                generate_page(
                    e.path, 
                    template_path=template_path, 
                    dest_path=dest_dir_path
                    )
            if e.is_dir():
                print(f'Iterate over {e.path} directory')
                generate_pages_recursive(
                    e.path,
                    template_path= template_path,
                    dest_dir_path=dest_dir_path
                    )
                