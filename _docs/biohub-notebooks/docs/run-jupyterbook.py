#!/usr/bin/env python

from livereload import Server, shell
import os

docs_dir = os.path.dirname(os.path.realpath(__file__))
source_dir = os.path.join(docs_dir, '_source')
build_dir = os.path.join(docs_dir)

# Should be - biohub-notebooks/docs/_build/html
output_dir = build_dir

server = Server()
server.watch(
    source_dir,
    shell('jupyter-book build -n --keep-going --builder html --path-output {} . '.format(output_dir), cwd=source_dir),
    delay=1,
)
server.serve(
    root='{}/_build/html'.format(output_dir),
    host='0.0.0.0',
    port=8003
)
