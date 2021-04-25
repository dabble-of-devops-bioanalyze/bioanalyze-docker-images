#!/usr/bin/env python

from cookiecutter.main import cookiecutter
import os
import json
import shutil

TEMPLATE = os.path.dirname(os.path.realpath(__file__))
TEMPLATE = os.path.join(TEMPLATE, 'templates')

with open('templates/cookiecutter.json', 'r') as reader:
    data = json.load(reader)

for pangeo_version in data['pangeo_versions']:

    data['pangeo_notebook_version'] = pangeo_version

    if pangeo_version = "2021.04.05":
        data['jupyterlab_version']="3"

    cookiecutter(
        TEMPLATE,  # path/url to cookiecutter template
        overwrite_if_exists=True,
        extra_context=data,
        output_dir='.',
        no_input=True
    )
