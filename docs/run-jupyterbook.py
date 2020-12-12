#!/usr/bin/env python

from livereload import Server, shell
import os

source_dir = "/docs/_source"
output_dir = "/docs/_build/jupyterbook"
server = Server()
server.watch(
    source_dir,
    shell('jupyter-book build -n --keep-going --builder html --path-output {} . '.format(output_dir), cwd=source_dir),
    delay=1,
)
server.serve(
    root='{}/_build/html'.format(output_dir),
    host='0.0.0.0',
    port=8001
)
