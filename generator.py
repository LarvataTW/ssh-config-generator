#!/usr/bin/env python3

import os
import re
import yaml
import argparse

from dotenv import load_dotenv, find_dotenv
from jinja2 import Environment, FileSystemLoader

# https://stackoverflow.com/questions/528281/how-can-i-include-a-yaml-file-inside-another
class Loader(yaml.SafeLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)


Loader.add_constructor('!include', Loader.include)

# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def debug(var):
    print(var)
    return ''

def generate_content(yaml_file, template_file):
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(
        loader=FileSystemLoader(os.path.join(THIS_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True
    )
    j2_env.filters['debug'] = debug

    with open(yaml_file) as yml:
        yml = yaml.load(yml, Loader)

    client_name = yml['clients'][0]['name']
    template_kind = os.path.splitext(os.path.basename(template_file))[0]
    template = j2_env.get_template(template_file)
    content = str(template.render(yml))
    content = re.sub('\\n[ ]+(?=\w)', '\n', content)
    content = re.sub(' +', ' ', content)

    return client_name, template_kind, content

def save_content(content, output, client_name=None, kind=None):
    if not output:
        output_kind = ''
        output_file = 'content'
        if kind == 'ssh':
            output_kind = 'ssh'
            output_file = 'config'
        elif kind == 'ansible':
            output_kind = 'ansible'
            output_file = 'hosts'
        output = 'output/{}/{}/{}'.format(output_kind, client_name, output_file)

        load_dotenv(find_dotenv())
        if kind == 'ssh' and os.getenv("SSH_OUTPUT"):
            output = os.getenv("SSH_OUTPUT")
        if kind == 'ansible' and os.getenv("ANSIBLE_OUTPUT"):
            output = os.getenv("ANSIBLE_OUTPUT")

    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))

    with open(output, 'w') as output:
        output.write(content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--template", help="Jinja2 template file.", default="templates/ssh.j2")
    parser.add_argument("-y", "--yaml", help="Values in a YAML file.")
    parser.add_argument("-o", "--output", help="Save output to a file.")
    args = parser.parse_args()

    client_name, template_kind, content = generate_content(args.yaml, args.template)
    save_content(content, args.output, client_name, template_kind)
