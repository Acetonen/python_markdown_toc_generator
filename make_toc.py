"""
Simple script to automatically generate table of content in markdown file.

python make_toc <FILE_PATH>
"""
import re
import click
from pathlib import Path


def write_to_file(file_path, content, table_of_content):
    new_file_content = [content[0], table_of_content] + content[1:]

    new_path = file_path.with_name(file_path.stem + '_TOC').with_suffix(file_path.suffix)
    new_path.write_text(''.join(new_file_content))


def change_deepenes(header, deepenes):
    item_deep = header.split(' ')[0].count('#')

    if len(deepenes)+1 > item_deep:
        deepenes.pop()

    elif len(deepenes)+1 < item_deep:
        deepenes.append(0)

    deepenes[-1] = deepenes[-1] + 1


def make_item(header):
    header_list = header.lower().split(' ')
    link = '#' + '-'.join(header_list[1:])
    title = ' '.join(header.split(' ')[1:])
    item = f"[{title}]({link})"

    return item


def make_table_of_content(headers_generator):
    deepenes = [0]
    table_of_content = ['## Table of Content']
    next(headers_generator)  # first item is main title, skip it.

    for header in headers_generator:
        item = make_item(header)

        change_deepenes(header, deepenes)

        table_of_content.append('{}{}. {}'.format((len(deepenes)-1) * '\t',
                                                  '.'.join(map(str, deepenes)),
                                                  item))

    return '\n'.join(table_of_content)


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def main(file_path, **kwargs):
    file_path = Path(file_path)
    assert file_path.suffix == '.md', "You must choose .md file!"

    with file_path.open() as file:
        content = file.readlines()

    headers_generator = (re.search(r'([#]+.*)', line).group() for line in content if re.search(r'([#]+.*)', line))

    table_of_content = make_table_of_content(headers_generator)

    write_to_file(file_path, content, table_of_content)


if __name__ == '__main__':
    main()
