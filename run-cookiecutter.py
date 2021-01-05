#!/usr/bin/env python

from cookiecutter.main import cookiecutter
import os
import json
import shutil

TEMPLATE = os.path.dirname(os.path.realpath(__file__))
TEMPLATE = os.path.join(TEMPLATE, 'templates')

with open('templates/cookiecutter.json', 'r') as reader:
    data = json.load(reader)

cookiecutter(
    TEMPLATE,  # path/url to cookiecutter template
    overwrite_if_exists=True,
    extra_context=data,
    output_dir='.',
    no_input=True
)
